# Problem Sets

This is your personal repository for Problem Sets!

If you are reading this, the name of the repository should be ps0-YourGithubID. If that's what you see, you should already be logged into your Github account and have your own private repository (this one) for your homeworks. You're good to read on!

If you don't see your Github ID at the end of the repository name, you need to follow [this link to Github Classroom](https://classroom.github.com/a/3UHVo2JF) to create your own private repository.

If you don't know what any of this means, come to office hours or send us a message on [Piazza](https://piazza.com/barnard/spring2023/comsbc3159)!

## How this repository works
This repository is a copy of a "seed" repository maintained by the course staff. Throughout this semester, we will add assignments to the seed repository, and you will be responsible for copying them into your local repository (using "fetch" and "merge", in git-speak). To get the repository set up for the semester please run:
```
git branch -M main
git remote add seed_repo https://github.com/COMS-BC3159-SP23/psets.git
```
These commands (0) set the main branch name and (1) tell your local git repository where the seed repo is (and calls it "seed_repo"). You are now ready for the rest of the semester.

Later in the semester, assuming you've already cloned your repository locally using the Github Classroom link and run the above commands, you can get new files for subsequent assignments by running:
```
git fetch seed_repo
git merge seed_repo/main -m "Fetched new assignment"
```
These commands (0) get the latest assignment from github.com, and (1) merges it with your local files.

## Problem set rules
Each problem set will consist of a written and programming portion. This course’s policy on academic honesty builds on the honor code and is best stated as "be reasonable." We recognize that interactions with classmates and others can facilitate mastery of the course’s material. However, there remains a line between asking for help and submitting someone else’s work. For individual assignments students are permitted to ask classmates and others for conceptual help so long as that help does not reduce to another doing your work for you (e.g., writing your response, copy-pasting code, or making your slides). Please review the Academic Integrity section of the syllabus for more information.

## Problem set submission
Make sure to submit your final written PDF to [Gradescope](https://www.gradescope.com/courses/489410) as well as you final **modified** code files. When you complete the assignment (and honestly at any major checkpoint) you should always push your code to this repository so that your code is backed up. You can do this by running:
```
git add .
git commit -m "<commit message goes here"
git push
```

## Finally
If you are having any trouble, please reach out to us, we're here to help!
