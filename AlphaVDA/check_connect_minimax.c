// check_connect.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int check_connect_minimax(int* board, int rows, int cols,  int max_connect, int base) {
    int connect_counter;
    int reward = 0;

    for(int i = 0; i < rows; i++){
        for(int j = 0; j < cols; j++){

            // Check rows
            connect_counter = 0;
            if(i == 0 || board[(i - 1)*cols + j] == 0){
                for(int k = 0; k < max_connect; k++){
                    if(i + k < rows && board[(i + k)*cols + j] == 1){
                        connect_counter += 1;
                    }else{
                        break;
                    }
                }
            }
            if(connect_counter > 1){
                reward += (int) pow(base, connect_counter - 1);
            }

            // Check cols
            connect_counter = 0;
            if(j == 0 || board[i*cols + j - 1] == 0){
                for(int k = 0; k < max_connect; k++){
                    if(j + k < cols && board[i*cols + j + k] == 1){
                        connect_counter += 1;
                    }else{
                        break;
                    }
                }
            }
            if(connect_counter > 1){
                reward += (int) pow(base, connect_counter - 1);
            }

            // Check diagonal1
            connect_counter = 0;
            if((i == 0 && j == 0) || board[(i - 1)*cols + j - 1] == 0){
                for(int k = 0; k < max_connect; k++){
                    if(i + k < rows && j + k < cols && board[(i + k)*cols + j + k] == 1){
                        connect_counter += 1;
                    }else{
                        break;
                    }
                }
            }
            if(connect_counter > 1){
                reward += (int) pow(base, connect_counter - 1);
            }

            // Check diagonal2
            connect_counter = 0;
            if((i == rows - 1 && j == 0) || board[(i + 1)*cols + j - 1] == 0){
                for(int k = 0; k < max_connect; k++){
                    if(i - k >= 0 && j + k < cols && board[(i - k)*cols + j + k] == 1){
                        connect_counter += 1;
                    }else{
                        break;
                    }
                }
            }
            if(connect_counter > 1){
                reward += (int) pow(base, connect_counter - 1);
            }

        }
    }
    return reward;
}
