# community-currency-reframery

How to setup and run server (prototype 2)
1. Install requirements.txt
2. cd into the backend directory
3. Make db migration:
python manage.py makemigrations
4. Migrate db
python manage.py migrate
5. Open postman and make a post request to /register endpoint to create a user
6. Open python shell and edit user's wallet manually to use contract owner ethereum private key (this use currently holds 99% of DANC tokens). Private key can be found in /backend/reframery/services/eth-config test account 1. 
python manage.py shell
