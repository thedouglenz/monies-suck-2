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
8. run **foreman start**
9. create a file called '.env' in the project directory
10. the next instruction is going to require you to setup a postgresql database so do that now
11. Fill it with 2 separate lines: 'DATABASE_URL=postgres://<dbpassword>:<dbuser>@localhost/<dbname>' (replacing <...> with appropriate values) and 'PORT=5000' (that's the second line to put in .env)
12. You will want to ignore the venv/ directory and this .env file in the .gitignore file in the project directory
13. visit localhost:5000/create_db to generate the database
14. visit localhost:5000 to see the application



