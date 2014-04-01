Ghassen and Bumsoo (Matt and Carolyn too), here are the instructions using
which you guys can see/test/play-with the frontend code I've written so far.
I have used the frontend framework called 'AngularJS' developed by Google. 

prereqs
- you will need 'node.js' and 'npm'
- 'npm' is a package manager for 'node.js'
- why will you need these things? well, we're gonna be testing the code using 'localhost:8000',
  right? so basically, the people who made angularjs also made a very simple barebones server
  which simply serves html/css/js/json/whatever files from various directories on the local
  machine. they wrote this server using javascript, and so obviously we need to run that 
  server using nodejs

next steps
- now go to https://github.com/angular/angular-seed
- follow the instructions in README.md until you encounter the 'Directory Layout' heading
  in these instructions. this heading and everything after this heading is not important
  NOTE: one of the first steps in these directions is to run a 'git clone'. dont run this
  command when you're inside Ghassen's cloned 333 directory, because it might mess things
  up. so basically, run the 'git clone' in an entirely separate folder. you will notice
  that a folder with the name 'angular-seed' will be created.
- navigate to 'angular-seed/app' and delete everything in this folder. delete EVERYTHING. 
- and now, go back to Ghassen's 333 directory. naviagate to '333/frontend'
- copy EVERYTHING from '333/frontend' and paste it in 'angular-seed/app'
- navigate to 'angular-seed'
- run the command 'npm start'
- open Chrome and go to "localhost:8000/app/index.html"
- TADA!! :)
