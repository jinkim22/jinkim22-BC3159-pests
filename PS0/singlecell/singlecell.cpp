// The main function that calls your functions.

#include "util.h"

// the main game backend function
void singlecell(){
    // Allocate memory DYNAMICALLY for N characters to be in the game
    Character *characters;
    allocate_memory(&characters,N_CHARACTERS);

    // Generate initial characters
    for (int i = 0; i < N_CHARACTERS; i++){
      characters[i].id = i;
      characters[i].size = starting_size;
      characters[i].x = getRand<int>();
      characters[i].y = getRand<int>();
      characters[i].alive = 1;
    }

    // Run all moves
    for (int move = 0; move < TOTAL_MOVES; move++) {
        // First we apply the moves
        apply_moves(characters, ALL_MOVES[move]);

        // Then we check for and resolve collisions
        check_resolve_all_collision(characters);
    }

    // Print the final locations, ids, and sizes of the surviving characters
    for (int i = 0; i < N_CHARACTERS; i++){
      if (characters[i].alive){
        printf("[%d] at (%d,%d) with size [%d]\n",characters[i].id,
                                                  characters[i].x,
                                                  characters[i].y,
                                                  characters[i].size);
      }
    }

    // Don't forget to free any memory you allocated!
    free(characters);
}

int main() {
    singlecell();
    return 0;
}