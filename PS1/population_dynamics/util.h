#include "helpers.h"
// I suggest testing with this set to 1 first!
#define MAX_THREADS 8

// function to simulate population change for one community of one species
//
// Note: 1) The change in population for a community is proportional to 
//          its growth_rate and local_population_share
//       2) If it has collected enough food to feed the population it grows, else it shrinks
//       3) If the population drops below 5 it goes extinct
void update_community_population(Species_Community *communities, int community_id, float local_population_share) {
  //
  // # TODO: add implementation
  //
}

// function to find the local population share for one community of one species
//
// Note: 1) Population share is defined as the percentage of population in a region
//          that is a given species across all communities of all species
float compute_local_population_share(Species_Community *communities, int community_id){
  //
  // # TODO: add implementation
  //
}

// Updates the population for all communities of all species
//
// Note: 1) You will want to launch MAX_THREADS to compute this
//       2) You will need to use compute_local_population_share and update_community_population
//       3) Make sure your logic is thread safe! Warning there likely is a data dependancy!
//       4) Feel free to use helper functions if that makes your life easier!
void update_all_populations(Species_Community *communities){
  //
  // # TODO: add implementation
  //
}

// function to simulate food gathering
// 
// Note: 1) Each round food starts at 0 and each member of the population tries to collect food
//       2) Please use food_oracle() to get a new amount of food for each member of the population
//       3) Please use MAX_THREADS threads per Species_Community! (Not spread across them but for each one)
//       4) All other implementation details are up to you!
void gather_all_food(Species_Community *communities) {
  //
  // # TODO: add implementation
  //
}

// the main function
//
// Hints: gathers food and updates the population for everyone
//        for NUM_TIME_PERIODS
void population_dynamics(Species_Community *communities){
  //
  // # TODO
  //
}