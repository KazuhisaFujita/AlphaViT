// check_connect.c
#include <stdio.h>


int check_valid(int* board, int rows, int cols, int x, int y, int player) {
    int directions[8][2];

    directions[0][0] =  1;
    directions[0][1] =  0;
    directions[1][0] =  1;
    directions[1][1] =  1;
    directions[2][0] =  0;
    directions[2][1] =  1;
    directions[3][0] = -1;
    directions[3][1] =  1;
    directions[4][0] = -1;
    directions[4][1] =  0;
    directions[5][0] = -1;
    directions[5][1] = -1;
    directions[6][0] =  0;
    directions[6][1] = -1;
    directions[7][0] =  1;
    directions[7][1] = -1;

    int valid = 0;
    for(int i = 0; i < 8; i++){
        int row = x + directions[i][0];
        int col = y + directions[i][1];
        if(row >=0 && col >= 0 && row < rows && col < cols){
            if(board[row*cols + col] == player*(-1)){
                while(1){
                    row += directions[i][0];
                    col += directions[i][1];
                    if(row >=0 && col >= 0 && row < rows && col < cols){
                        if(board[row*cols + col] == player){
                            valid = 1;
                            break;
                        }else if(board[row*cols + col] == 0){
                            break;
                        }
                    }else{
                        break;
                    }
                }
            }
        }
    }


    return valid;
}
