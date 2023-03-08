# COMS BC 3159 - SP23
# PS1: Parallel Programming on the CPU and GPU
* Due: 11:59pm Monday, February 13th

## Submission Information

**This year for submission we are using Gradescope - you must submit to [Gradescope](https://www.gradescope.com/courses/489410) to get credit!** Gradecope will allow for infinite submissions until the deadline and then will start marking submissions as late and will then lock 2 days after the due date. Please make sure to mark the page for each question on the written via Gradescope and only upload the requested files for the code section. Also if you are having issues with autograders make sure you didn't rename files! Submissions not following the requirements *will not be graded* so make sure to ask quesitons before the deadline!

**NOTE: There is no autograder for PS1 -- please submit code to Courseworks!!!**

Good luck!

## Written Assignment (20 points)

Please go to the PDF in the `written` folder for the written instructions (also available on Gradescope). Please use the provided latex template to write up your solutions and *submit the pdf output from latex to Gradescope*. Please refer to the software install guide for more information on Latex.

## Coding Assignment (20 points)

You will find both a `population_dynamics` and `gpu_population_dynamics` folder in this repository that each house half of the coding assignment. Your goal here is both using parallel C++ on the CPU, as well as CUDA C++ on the GPU, implement a population dynamics simulation by filling in the starter code. Note that the problems are nearly identical and for some functions only minor modificaitons (if any) need to be made between the two solutions. Also note that your code does not need to be perfectly optimized, it just needs to be correct and implement the specification. That said, if you can do the right things with memory access patterns and write overall efficient code that will make us happy when we grade! Who knows, we may even decide to give out a bonus point! :)