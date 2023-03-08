// Some helper functions and other constants

#include <iostream>
#include <random>

// Helpful constants
const int N_CHARACTERS = 20;
const int starting_size = 2;
const int xy_max = 25;
const int xy_min = -25;

// random helpers
std::default_random_engine randEng(1337);
std::normal_distribution<double> randDist(0, 10); //mean followed by stdiv
template <typename T>
T getRand(){return static_cast<T>(randDist(randEng));}

// distance helper
template <typename T>
T euclidean_distance(T x1, T y1, T x2, T y2){return sqrt(pow(x2-x1,2)+pow(y2-y1,2));}

// A struct can be thought of as a barebones class that can be used to define
// a compact new type. For example this one below defines a character that
// packs together all the important characteristics we need to track. 
// Here is a short blog post on structs vs. classes: 
// https://www.geeksforgeeks.org/structure-vs-class-in-cpp/
struct Character {
    int id;
    int size;
    int x;
    int y;
    int alive; // 1 for alive and 0 for dead
};