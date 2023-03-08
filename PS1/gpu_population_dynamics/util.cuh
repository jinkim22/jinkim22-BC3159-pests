#include "helpers.cuh"
// I suggest testing with these set to 1 first!
#define NUM_BLOCKS 1
#define NUM_THREADS TOTAL_COMMUNITIES


// function to simulate population change for one community of one species
//
// Note: 1) The change in population for a community is proportional to 
//          its growth_rate and local_population_share
//       2) If it has collected enough food to feed the population it grows, else it shrinks
//       3) If the population drops below 5 it goes extinct
//
// Hint: this should remain basically unchanged from the CPU version (depending on the rest of your implementation)
__device__
void update_community_population(Species_Community *s_communities, int community_id, float local_population_share) {
  //
  // # TODO
  //
}

// function to find the local population share for one community of one species
//
// Note: 1) Population share is defined as the percentage of population in a region
//          that is a given species across all communities of all species
//
// Hint: this should remain basically unchanged from the CPU version (depending on the rest of your implementation)
__device__
float compute_local_population_share(Species_Community *s_communities, int community_id){
  //
  // # TODO
  //
}

// Updates the population for all communities of all species
//
// Note: 1) You will need to use compute_local_population_share and update_community_population
//       3) Make sure your logic is thread safe! Again this is likely to have a race condition!
//       4) Feel free to use helper functions if that makes your life easier!
__device__
void update_all_populations(Species_Community *communities){
  //
  // # TODO
  //
}

// function to simulate food gathering
// 
// Note: 1) Each round food starts at 0 and each member of the population tries to collect food
//       2) Please use food_oracle() to get a new amount of food for each member of the population
//       3) You can allocate threads to communites however you want!
//       3) All other implementation details are up to you! (Don't worry if your design isn't perfect!)
__device__
void gather_all_food(Species_Community *s_communities) {
  //
  // # TODO
  //
}

// the main kernel that computes the population dynamics over time
//
// Hints: 1) using shared memory may speed things up
//           but then make sure to save things back to RAM
//        2) make sure you do all NUM_TIME_PERIODS of gather_all_food
//           and update_all_populations
__global__
void population_dynamics_kernel(Species_Community *d_communities){
  //
  // # TODO
  //
}

// the main function
//
// Hints: set up GPU memory, run the kernel, clean up GPU memory
__host__
void population_dynamics(Species_Community *h_communities){
  //
  // #TODO
  //
}