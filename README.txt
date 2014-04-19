guys, none of us have used git before, and so everything has gotten a little
messed up, but i promise to clean it all up and have the new frontend and
the new backend both working properly in the same branch (and no merge issues
and shit) before our meeting with raghav on monday. if i get done with 340
homework early, then i might be able to solve this by sunday evening. :)

--- SKETCHY INSTRUCTIONS, MOSTLY WONT WORK WITHOUT A COUPLE MODIFICATIONS ---

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

some things:

1. the main starting html file is in 333/princeton-marketplace/market/templates/market/index.html
2. dont ever run collectstatic
3. all static files are manually stored in 333/princeton-marketplace/static/
4. put all css code in 333/princeton-marketplace/static/css/index.css
5. put all js code in 333/princeton-marketplace/static/js/index.js
6. please please please make clear, commented, modular changes in the right places. 
7. write your name with the comment too if possible so everyone knows who to talk to when he doesn't understand something

if you think i'm doing something blatantly wrong/unacceptable in the frontend,
just let me know on facebook! 
