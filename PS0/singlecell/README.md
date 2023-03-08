# PS0: C++ Singlecell Game Backend Assignment

## Problem Statement
You are tasked with creating a program that simulates a modifed version of the [Agar.io](http://agar.io/) game using C++. We have provided some starter code for you, and your job is to fill in the missing code as specified by the `#TODO#` blocks in the code. You can either just work in the ipynb OR you can work locally with the various files in this folder.

## Game Description
In this version of the game, each character starts as a circle with a fixed size (radius) in a random location on a 2D grid. Each character is given a unique ID indicating when they joined the game. IDs start at 0 and increase over time.

On each turn, each of the characters remaining in the game can move either up, down, left, or right by one unit. For this version of the game those moves are set at compile time and constant for all characters. Characters that run into walls (as defined by the max and min xy values bounce off of the walls and stay put.

When characters run into each other, one of two things happens:
1. If the characters are different sizes, the smaller character is removed from the game and the larger character wins and grows in size by the size of the smaller character. For example, if a character of size 3 runs into a character of size 2, the character of size 2 is removed from the game and the character of size 3 becomes size 5.

2. If the characters are the same size, the character that joined the game first (has a smaller `id`) wins and grows in size as described above.

At the end of the game your code should print the final surviving characters, their ID, location, and size.

## Functions You'll Need To Implement (2 Points Each)
All functions you need to implement are in `util.h` and that is the only file you need to submit to gradescope!
+ `allocate_memory`
+ `apply_moves`
+ `in_collision`
+ `resolve_collision`
+ `check_resolve_all_collision`

## Submission
Once you are done, download and submit (or just submit if you are working locally) your `singlecell.h` file to [Gradescope](https://www.gradescope.com/courses/489410). Unfortunately we do not yet have an autograder for this assignment and so we will grade this manually unless we can get one developed in time. If we do get one developed remember that you can submit assingments to the autograder as many times as you would like before the deadline!

## Notes and Hints
+ **DO NOT CHANGE FUNCTION DEFINITIONS** or you will break our grading scripts
+ When implementing your code make sure to break ties based on id and evaluate all of the possible collisions in id order! That is, first check if id=0 collides with all other characters before moving onto id=1! (This is just so that the grading scripts and example outputs work correctly).
+ If your code is implemented correctly and follows the note above then the text below will show you what the result should be for the given `moves.h` file.
+ See the syllabus for our course collaboration policy (long story short you are welcome to collaborate at a high level but please do not copy each others code).
+ If you are working in Colab, you can change the formatting of the code to different color schemes: just change the `%%cpp -n <filename>.h -s xcode` to a different `-s` flag. The list can be [found at this link](https://gist.github.com/akshaykhadse/7acc91dd41f52944c6150754e5530c4b).
+ Please reach out on Piazza with any and all questions!