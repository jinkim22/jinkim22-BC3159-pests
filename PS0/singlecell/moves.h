// Hard-coded moves
// Note: 0 = Up, 1 = Down, 2 = Left, 3 = Right
const int ALL_MOVES[] = {0,1,3,2,0,0,1,2,1,0,0,0,1,1,0,0,3,0,2,1};
const int TOTAL_MOVES = 20;

// These moves should get the following output:
// [10] at (4,1) with size [40]
// If you instead get the following output (or something else with lots of very very large sizes) you aren't handling characters being alive or dead correctly! Note that as we start with 20 characters of size 2 the total size should be 40!
// [6] at (-6,3) with size [16]
// [7] at (12,2) with size [24]
// [8] at (-3,-16) with size [32]
// [10] at (4,1) with size [24]
// [11] at (18,2) with size [32]
// [12] at (22,11) with size [32]
// [13] at (21,23) with size [32]
// [14] at (-17,-2) with size [30]
// [15] at (16,19) with size [32]
// [17] at (8,6) with size [16]
// [18] at (1,0) with size [24]
// [19] at (-1,2) with size [16]
