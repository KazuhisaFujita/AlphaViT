#---------------------------------------
#Since : 2019/04/08
#Update: 2024/10/05
# -*- coding: utf-8 -*-
#---------------------------------------
# Import required libraries
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.utils.data import Dataset, DataLoader, DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.cuda.amp as amp

import os
import shutil
import time
import random
import numpy as np
import math
import sys

import torch.optim as optim
from torchvision import datasets, transforms

from parameters_alphavit import Parameters

class Net(nn.Module):
    def __init__(self, params = Parameters()):
        super().__init__()
        self.params = params

        self.patch_embedding  = nn.Conv2d(self.params.input_channels, self.params.emb_size, kernel_size=self.params.patch_size,
                                          stride=self.params.stride_size, padding = (self.params.patch_size-1)//2)

        # transformer encoder
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model   = self.params.emb_size,
            nhead     = self.params.num_heads,
            activation= 'gelu',
            dropout = self.params.dropout,
            dim_feedforward = self.params.dim_feedforward,
            batch_first=True,
            norm_first=True
            )

        self.transformer_encoder = nn.TransformerEncoder(
            self.encoder_layer,
            num_layers=self.params.num_layers,
            enable_nested_tensor=False
            )

        # Class token
        self.value_token = nn.Parameter(torch.randn(1,1, self.params.emb_size))
        self.game_token = torch.zeros((1,1,self.params.emb_size))

        # Positional encoding
        self.positional_embedding = nn.Parameter(torch.randn(1, self.params.emb_size, self.params.pos_size**2))

        # dropout befor addition of the cls token
        self.dropout = nn.Dropout(p=self.params.dropout)

        # Value head
        self.value_head = nn.Sequential(
            nn.LayerNorm(self.params.emb_size),
            nn.Linear(self.params.emb_size, self.params.num_value_hidden),
            nn.GELU(),
            nn.Linear(self.params.num_value_hidden, 1),
            nn.Tanh()
        )

        # Pass token
        self.pass_token = nn.Parameter(torch.randn(1, 1, self.params.emb_size))

        # Policy head
        self.policy_head = nn.Sequential(
            nn.LayerNorm(self.params.emb_size),
            nn.Linear(self.params.emb_size, self.params.num_policy_hidden),
            nn.GELU(),
            nn.Linear(self.params.num_policy_hidden, 1)
        )

    def forward(self, input):
        device = input.device

        B, C, W, H = input.shape

        pos_embedding2d       = self.positional_embedding.view(-1, 1, self.params.pos_size, self.params.pos_size)
        padding_row           = (self.params.patch_size - 1)//2
        padding_col           = (self.params.patch_size - 1)//2
        grid_size             = (math.floor((W + 2*padding_row - self.params.patch_size) // self.params.stride_size) + 1,
                                 math.floor((H + 2*padding_col - self.params.patch_size) // self.params.stride_size) + 1)
        pos_embedding         = F.interpolate(pos_embedding2d, size = (grid_size[0], grid_size[1]), mode='bilinear', align_corners=False)
        pos_embedding         = pos_embedding.view(-1, self.params.emb_size, grid_size[0]*grid_size[1])
        pos_embedding         = pos_embedding.transpose(1, 2)

        x = self.patch_embedding(input)
        x = x.flatten(2)      # (B, E, H*W)
        x = x.transpose(1, 2) # (B, H*W, E)

        x = x + pos_embedding

        # Append class token.
        game_tokens = self.game_token.to(device).expand(B, -1, -1)  # expand the class token to the batch size
        x = torch.cat((game_tokens, x), dim=1) # (B, N + 1, E)
        value_tokens = self.value_token.expand(B, -1, -1)  # expand the class token to the batch size
        x = torch.cat((value_tokens, x), dim=1) # (B, N + 1, E)
        pass_tokens = self.pass_token.expand(B, -1, -1)  # expand the class token to the batch size
        x = torch.cat((x, pass_tokens), dim=1) # (B, N + 1, E)

        x = self.dropout(x)
        x = self.transformer_encoder(x)

        # Extract the class token.
        v = x[:,0]
        v = self.value_head(v)

        p = x[:,2:]
        p = self.policy_head(p)
        p = p.squeeze(-1)
        p = F.log_softmax(p, dim=1)

        return p, v

class NNetWrapper:
    def __init__(self, params = Parameters(), device = 'cuda'):
        self.params = params
        self.net = Net(params)
        self.device = device

    def predict(self, states, game_name):

        self.net.game_token = self.params.game_token[game_name]

        device = torch.device(self.device)
        self.net.to(device)

        board = torch.Tensor(states).to(device)

        self.net.eval()
        with torch.no_grad():
            # FP16
            with amp.autocast():
                pi, v = self.net(board.unsqueeze(0))

        return torch.exp(pi).detach().to('cpu').numpy()[0], v.item()


    def train(self, training_board, training_prob, training_v, games):
        # mixed precision
        scaler = amp.GradScaler()

        device = torch.device(self.device)
        model = nn.DataParallel(self.net, device_ids=[0,1])

        model.to(device)

        training_boards = {}
        training_probs  = {}
        training_vs     = {}
        train_loaders = {}
        train_loader_iters = {}

        for game_name in games:
            training_boards[game_name] = torch.Tensor(np.array(training_board[game_name].Get_buffer_start_end()))
            training_probs[game_name]  = torch.Tensor(np.array(training_prob[game_name].Get_buffer_start_end()))
            training_vs[game_name]     = torch.Tensor(np.array(training_v[game_name].Get_buffer_start_end()))

            ds_train    = torch.utils.data.TensorDataset(training_boards[game_name], training_probs[game_name], training_vs[game_name])
            train_loaders[game_name] = torch.utils.data.DataLoader(ds_train, batch_size = self.params.batch_size, shuffle=True, num_workers = 1, pin_memory = True)

        #optimizer    = optim.SGD(model.parameters(), lr = self.params.lam, weight_decay = self.params.weight_decay, momentum = self.params.momentum)
        optimizer = optim.AdamW(model.parameters(), lr=self.params.lam)

        # variable in order to print losses
        self.total_loss = 0
        self.lo_pi      = 0
        self.lo_v       = 0
        counter         = 0

        total_l = 0
        for epoch in range(self.params.epochs):
            model.train()

            for game_name in games:
                train_loader_iters[game_name] = iter(train_loaders[game_name])

            for _ in range(len(train_loaders[games[0]])):
                for game_name in games:
                    model.game_token = self.params.game_token[game_name]

                    boards, pis, vs = next(train_loader_iters[game_name])
                    boards, pis, vs = boards.to(device), pis.to(device), vs.to(device)
                    # out_pis, out_vs = model(boards)

                    # l_pi = self.loss_pi(pis, out_pis)
                    # l_v  = self.loss_v(vs, out_vs)
                    # total_l = l_pi + l_v

                    # optimizer.zero_grad()
                    # total_l.backward()
                    # optimizer.step()

                    # FP16
                    with amp.autocast():
                        out_pis, out_vs = model(boards)

                        l_pi = self.loss_pi(pis, out_pis)
                        l_v  = self.loss_v(vs, out_vs)
                        total_l = l_pi + l_v

                    optimizer.zero_grad()
                    scaler.scale(total_l).backward()
                    scaler.step(optimizer)
                    scaler.update()

                    self.total_loss += total_l.item()
                    self.lo_pi      += l_pi.item()
                    self.lo_v       += l_v.item()
                    counter         += 1

        self.total_loss /= counter
        self.lo_pi      /= counter
        self.lo_v       /= counter

        self.net.to('cpu')
        torch.cuda.empty_cache()

    def loss_pi(self, targets, outputs):
        return -torch.sum(targets * outputs)/targets.size()[0]

    def loss_v(self, targets, outputs):
        return torch.sum((targets - outputs.view(-1)) ** 2)/targets.size()[0]

    def save_checkpoint(self, i = None):
        if i == None:
            torch.save(self.net.state_dict(), "checkpoint.model")
        else:
            torch.save(self.net.state_dict(), "checkpoint_" + str(i) + ".model")

    def load_checkpoint(self, i = None):
        if i == None:
            self.net.load_state_dict(torch.load("checkpoint.model"))
        else:
            self.net.load_state_dict(torch.load("checkpoint_" + str(i) + ".model"))
        self.net.eval()

    def load_model(self, f):
        self.net.load_state_dict(torch.load(f))
        self.net.eval()
