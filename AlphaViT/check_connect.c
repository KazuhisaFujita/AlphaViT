// check_connect.c
#include <stdio.h>

int check_connect(int* board, int rows, int cols, int connect) {
    int num_connect;

    for(int i = 0; i < rows; i++){
        for(int j = 0; j < cols; j++){

            // Check rows
            num_connect = 0;
            for(int k = 0; k < connect; k++){
                if(i + k < rows && board[(i + k)*cols + j] == 1){
                    num_connect += 1;
                }else{
                    break;
                }
            }
            if(num_connect >= connect){
                return 1;
            }

            // Check cols
            num_connect = 0;
            for(int k = 0; k < connect; k++){
                if(j + k < cols && board[i*cols + j + k] == 1){
                    num_connect += 1;
                }else{
                    break;
                }
            }
            if(num_connect >= connect){
                return 1;
            }

            // Check diagonal1
            num_connect = 0;
            for(int k = 0; k < connect; k++){
                if(i + k < rows && j + k < cols && board[(i + k)*cols + j + k] == 1){
                    num_connect += 1;
                }else{
                    break;
                }
            }
            if(num_connect >= connect){
                return 1;
            }

            // Check diagonal2
            num_connect = 0;
            for(int k = 0; k < connect; k++){
                if(i - k >= 0 && j + k < cols && board[(i - k)*cols + j + k] == 1){
                    num_connect += 1;
                }else{
                    break;
                }
            }
            if(num_connect >= connect){
                return 1;
            }

        }
    }

    return 0;
}
