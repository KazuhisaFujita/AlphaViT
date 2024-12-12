// bitboard_operations.c
#include <stdint.h>

void to_bitboard(int* board, int num, int white, int black, uint64_t* bb0, uint64_t* bb1) {
    *bb0 = 0;
    *bb1 = 0;
    for (int i = 0; i < num; i++) {
        for (int j = 0; j < num; j++) {
            *bb0 <<= 1;
            *bb1 <<= 1;
            int value = board[i * num + j];
            if (value == white) {
                *bb0 |= 1;
            } else if (value == black) {
                *bb1 |= 1;
            }
        }
    }
}
