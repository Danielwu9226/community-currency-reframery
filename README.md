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
7. Open python shell and edit user's wallet manually to use contract owner ethereum private key (this use currently holds 99% of DANC tokens). Private key can be found in 
/backend/reframery/services/eth-config test_accounts[account1]. (Don't worry, we are only interacting with the test ethereum network haha)
```
python manage.py shell
>>> from reframery.models import CustomUser, Wallet
>>> user = CustomUser.objects.all()[0]
>>> user.wallet.private_key = 0x59d4b4d333838d5d79463c502296725137ef3b2d2a2032f75923f1ab0468fdae
>>> user.wallet.address = 0x8691359B52337e86dA2Bad4483C4933156b65Fa6
```
8. Now make a second test user using /register endpoint via postman
9. Make a post request to the /transfer endpoint with 'user1's email', 'user2's email', and transfer amount in the request to transfer DANC coins from the first user to the second user.
10. Search for the transaction hash from the response in etherscan https://ropsten.etherscan.io/. (Might have to wait 30 seconds for the transaction to show up) 
