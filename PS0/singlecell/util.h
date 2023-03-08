// #TODO# The Code You Will Need To Edit


#include "moves.h"
#include "helpers.h"

// Allocates memory using malloc for an array of characters
void allocate_memory(Character** characters, int N_CHARACTERS){
  //
  // #TODO# 
  // Hint: You've been passed in a pointer to the location
  //       where we want to have an array's worth of memory.
  //       If this is wrinkling your brain this stackoverflow
  //       post may have some very valuable advice:
  //       https://stackoverflow.com/questions/897366/how-do-pointer-to-pointers-work-in-c-and-when-might-you-use-them
  //
}

// Applies the given move to all characters
// Note: 0 = Up, 1 = Down, 2 = Left, 3 = Right
void apply_moves(Character* characters, int move){
  //
  // #TODO#
  //
  return;
}

// returns True if in collision
bool in_collision(Character& c1, Character& c2){
  //
  // #TODO#
  // hint: the euclidean_distance function will be helpful and don't
  //       forget characters are circles!
  //
  return false;
}

// resolve a collision between two characters
void resolve_collision(Character& c1, Character& c2){
  //
  // #TODO#
  // hint: make sure to break ties correctly!
  //
  return;
}

// check for and resolve all possible collisions
void check_resolve_all_collision(Character* characters){
  //
  // #TODO#
  // Hint: a modified version of the following code will be helpful
  //       when called correctly inside of some loops and conditionals
  //       if (in_collision(c1, c2)){resolve_collision(c1,c2);}
  //
}