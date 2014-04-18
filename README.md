guys, this is a new branch and it has diverged from the original "master". 
that is because i didn't want to break our old very-ugly frontend. you don't have to
do anything special to have a look at this. instructions: 

1. go to 333/
2. make sure that you don't have any changes pending for commit
3. do "git pull origin greatlooks"
4. edit settings.py with you local MySQL server password
5. run dev_appserver.py
6. go to localhost:8080
7. be amazed :)

now, you'll realize that the most updated backend is in the "master" branch
and the most update frontend is in the "greatlooks" branch. we will worry about
merging after the TA meeting on Monday. in the meantime, if you want to switch 
branches, this is what you do:

1. do "git status"
2. note the name of the branch you are in (say master) and make sure you don't have pending commits
3. do "git checkout greatlooks"
4. this will change the entire 333/ directory
5. to switch back, make sure there are no pending commits
6. do "git checkout master"

if you think i'm doing something blatantly wrong/unacceptable in the frontend,
just let me know on facebook! 
