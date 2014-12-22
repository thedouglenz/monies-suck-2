monies-suck-2
=============

A better implementation of a previously written (unfinished) financial management app

## Dev setup instructions
If you want to contribute to this project you will need to set up your environment. This write-up assumes you're using either Ubuntu or OSX. To test locally, you will want to have a local postgres server running. On OS X, http://postgresapp.com/. On Ubuntu, you will have to fend for yourself but this will help: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04 

### Running locally
1. Make sure you have pip, and virtualenv installed globally on your system.
2. Clone this repo
3. Goto the project directory
4. run **virtualenv venv**
5. **source venv/bin/activate**
6. **pip install -r requirements.txt**
7. Install the heroku toolbelt globally on whatever system you are on: https://toolbelt.heroku.com/
8. create a file called '.env' in the project directory
9. setup a local postgresql server along with a database, user, and password
10. Fill the file .env with 2 separate lines: 'DATABASE_URL=postgres://<dbpassword>:<dbuser>@localhost/<dbname>' (replacing <...> with appropriate values) and 'PORT=5000' (that's the second line to put in .env)
11. You will want to ignore the venv/ directory and this .env file in the .gitignore file in the project directory
12. run **foreman start**
13. visit localhost:5000/create_db to generate the database
14. visit localhost:5000 to see the application

### Why do we do all the things above?

Following is an explanation of each item above:

1. These should belong to any python developer's toolbox
2. You have to have the files
3. To run some commands and to work in that directory now and in the future
4. This creates a "virtual environment" where you can install a bunch of python dependencies in a container as opposed to globally to your system. It's great for working on many projects that require different dependencies or different versions of them than other projects
5. This essentially "turns on" the virtualenv you've created here in this project
6. pip will read requirements.txt, that comes with this project, line by line and install all the dependencies for you!
7. The heroku toolbelt comes with a local deployment helper called foreman. You don't need to push up to a heroku instance necessarily to test this. It can run locally on your machine with the help of foreman
8. foreman will run your app according to the rules in Procfile and using your .env file for environment variables
9. A postgresql server is essential for this project as the webb application connects to a postgres instance to save its data
10. This file contains environment variables that mimick those that you could set on heroku if this were not being run locally
11. Those files don't need to be pushed to github or heroku because they're just for setting up your local environment
12. The application will start because of this. It will look at your Procfile for instructions on how to start the app as well as .env for your environment variables
13. This is a local first-time maneuver to set up the schema. It never really needs to be done more than once
14. This is so that you can see the application, test what you've done, and think about what you're going to do next
