# community-currency-reframery

How to setup and run server (prototype 2)
1. Install requirements.txt
2. cd into the backend directory
3. Make db migration:
```
python manage.py makemigrations
```
4. Migrate db
```
python manage.py migrate
```
5. Start server
```
python manage.py runserver
```
6. Open postman and make a post request with 'email' and 'password' fields in the request to the /register endpoint to create a user

