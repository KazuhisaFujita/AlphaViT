#---------------------------------------
#Since : 2019/04/08
#Update: 2024/10/03
# -*- coding: utf-8 -*-
#---------------------------------------
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
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

from parameters_alphazero import Parameters

class BasicBlock(nn.Module):
    def __init__(self, num_filters):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(num_filters, num_filters, 3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(num_filters)
        self.conv2 = nn.Conv2d(num_filters, num_filters, 3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(num_filters)

    def forward(self, x):
        r = x
        h = self.conv1(x)
        h = self.bn1(h)
        h = F.relu(h)
        h = self.conv2(h)
        h = self.bn2(h)
        h = h + r
        h = F.relu(h)

        return h

class Net(nn.Module):
    def __init__(self, params = Parameters(), game_name="Othello"):
        self.params = params
        self.game_name = game_name

        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(self.params.input_channels, self.params.num_filters, 3, stride=1, padding=1)
        self.bn1   = nn.BatchNorm2d(self.params.num_filters)

        self.blocks = self._make_layer(self.params.num_res, self.params.num_filters)

        # policy head
        self.conv_p = nn.Conv2d(self.params.num_filters, self.params.num_filters_p, 1, stride=1)
        self.bn_p   = nn.BatchNorm2d(self.params.num_filters_p)
        self.fc_p = nn.Linear(self.params.num_filters_p * self.params.board_x[game_name] * self.params.board_y[game_name], self.params.action_size[game_name])

        # value head
        self.conv_v = nn.Conv2d(self.params.num_filters, self.params.num_filters_v, 1, stride=1)
        self.bn_v   = nn.BatchNorm2d(self.params.num_filters_v)
        self.fc_v1 = nn.Linear(self.params.num_filters_v * self.params.board_x[game_name] * self.params.board_y[game_name], 256)
        self.bn_v1 = nn.BatchNorm1d(256)
        self.fc_v2 = nn.Linear(256, 1)

    def forward(self, x):
        x = x.view(-1, self.params.k_boards * 2 + 1, self.params.board_x[self.game_name], self.params.board_y[self.game_name])
        h = F.relu(self.bn1(self.conv1(x)))

        h = self.blocks(h)

        # policy head
        h_p = F.relu(self.bn_p(self.conv_p(h)))
        h_p = h_p.view(-1, self.params.num_filters_p * self.params.board_x[self.game_name] * self.params.board_y[self.game_name])
        h_p = self.fc_p(h_p)
        p = F.log_softmax(h_p, dim=1)

        # value head
        h_v = F.relu(self.bn_v(self.conv_v(h)))
        h_v = h_v.view(-1, self.params.num_filters_v * self.params.board_x[self.game_name] * self.params.board_y[self.game_name])
        h_v = F.relu(self.bn_v1(self.fc_v1(h_v)))
        h_v = self.fc_v2(h_v)
        v = torch.tanh(h_v)

        return p, v

    def _make_layer(self, blocks, num_filters):
        layers = []
        for _ in range(blocks):
            layers.append(BasicBlock(num_filters))

        return nn.Sequential(*layers)


class NNetWrapper:
    def __init__(self, params = Parameters(), game_name="Othello", device = 'cuda'):
        self.params = params
        self.game_name = game_name
        self.net = Net(params = self.params, game_name = self.game_name)
        self.device = device

    def predict(self, states):
        device = torch.device(self.device)
        self.net.to(device)
        board = torch.Tensor(states).to(device)

        self.net.eval()
        with torch.no_grad():
            # FP16
            #with amp.autocast():
                pi, v = self.net(board)

        return torch.exp(pi).detach().to('cpu').numpy()[0], v.item()

    def train(self, training_board, training_prob, training_v):
        # mixed precision
        scaler = amp.GradScaler()

        device = torch.device(self.device)
        self.net.to(device)
        model = nn.DataParallel(self.net, device_ids=[0,1])

        training_board = torch.Tensor(training_board)
        training_prob = torch.Tensor(training_prob)
        training_v = torch.Tensor(training_v)

        ds_train = torch.utils.data.TensorDataset(training_board, training_prob, training_v)
        train_loader = torch.utils.data.DataLoader(ds_train, batch_size = self.params.batch_size, shuffle=True, num_workers = 1, pin_memory = True)
        optimizer = optim.SGD(model.parameters(), lr = self.params.lam, weight_decay = self.params.weight_decay, momentum = self.params.momentum)

        self.total_loss = 0
        self.lo_pi      = 0
        self.lo_v       = 0
        counter         = 0

        total_l = 0
        for epoch in range(self.params.epochs):
            model.train()

            for batch_idx, (boards, pis, vs) in enumerate(train_loader):

                boards, pis, vs = boards.to(device), pis.to(device), vs.to(device)

                out_pis, out_vs = model(boards)

                l_pi = self.loss_pi(pis, out_pis)
                l_v = self.loss_v(vs, out_vs)
                total_l = l_pi + l_v

                optimizer.zero_grad()
                total_l.backward()
                optimizer.step()

                # FP16
                # with amp.autocast():
                #     out_pis, out_vs = model(boards)

                #     l_pi = self.loss_pi(pis, out_pis)
                #     l_v = self.loss_v(vs, out_vs)
                #     total_l = l_pi + l_v

                # optimizer.zero_grad()
                # scaler.scale(total_l).backward()
                # scaler.step(optimizer)
                # scaler.update()

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
