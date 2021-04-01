from django.http import JsonResponse
import json 
from reframery.models import CustomUser, SubCategory, Order, Item, Wallet, Transaction
from reframery.models import CustomUser, Wallet
from reframery.services.ethService import generate_eth_account, transfer
from datetime import datetime
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.validators import validate_email


# Create your views here.

def checkInvalidRoutes(method, route_list):
    return method in route_list


def handleInvalidRouteJson():
    return JsonResponse({
        "message": "Invalid Method",
        "http_code": "400 Bad Request"
    })


def authFailedJson():
    return JsonResponse({
        "message": "Authentication Failed",
        "http_code": "401 Unauthorized",
    })


def verificationFailedJson():
    return JsonResponse({
        "message": "Invalid Verification Code.",
        "http_code": "401 Unauthorized"
    })


def checkIfUserExists(email):
    return len(CustomUser.objects.filter(email=email)) == 1


def getUser(email):
    return CustomUser.objects.filter(email=email)[0]

def getUserById(id):
    return CustomUser.objects.filter(id = id)[0]

def isInvalidVerificationCode(verification_code):
    return len(CustomUser.objects.filter(validate_code=verification_code)) != 1


def getUserFromVerificationCode(verification_code):
    return CustomUser.objects.filter(validate_code=verification_code)[0]

def getSubCategoryFromId(id):
    return SubCategory.objects.filter(id = id)[0]

def getItemById(id):
    return Item.objects.filter(id = id)[0]

def RegisterView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    
    params = ["email", "password"]
    validated_params = [param in data for param in params]
    if not all(validated_params):
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "401"
        })
    
    email = data['email']
    password = data['password']
    if checkIfUserExists(email):
        return JsonResponse({
            "message": "User already exists.",
            "http_code": "404"
        })
    try: 
        validate_email(email)
    except:
        return JsonResponse({
            "message": "Invalid email format",
            "http_code": "401"
        })
    user = CustomUser(email=email)
    user.set_password(password)
    user.save()

    # generate an eth account
    eth_account = generate_eth_account()
    eth_address = eth_account['address']
    eth_privateKey = eth_account['privateKey']
    # create eth wallet for user
    wallet = Wallet(customUser=user, address=eth_address, private_key=eth_privateKey)
    wallet.save()

    verification_code = user.validate_code

    return JsonResponse({
        "message": "User successfully created.",
        "http_code": "200",
        "jwt": user.token
    })


def LoginView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()

    data = json.loads(request.body)
    
    params = ["email", "password"]
    validated_params = [param in data for param in params]
    if not all(validated_params):
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "400"
        })
    
    email = data['email']
    password = data['password']
    if not checkIfUserExists(email):
        return authFailedJson()
    user = getUser(email)
    if not user.check_password(password):
        return authFailedJson()

    return JsonResponse({"jwt": user.token})


def ForgotPasswordView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()

    data = json.loads(request.body)
    params = ["email", "password"]
    validated_params = [param in data for param in params]
    if not all(validated_params):
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "400"
        })
    email = data['email']
    password = data['password']
    
    if len(password) == 0:
        return JsonResponse({
            "message": "Password cannot be empty",
            "http_code": "401"
        })
    
    if not checkIfUserExists(email):
        return authFailedJson()
    user = getUser(email)
    same_pass = user.check_password(password)
    if same_pass:
        return JsonResponse({
            "message": "Please enter a different password",
            "http_code": "403"
            })
    user.set_password(password)
    user.save()
    return JsonResponse({
        "message": "Password successfully changed.",
        "http_code": "200"
    })


def EmailConfirmationView(request, verification_code):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    
    if len(verification_code) == 0:
        return JsonResponse({
                "message": "No verification code specified",
                "http_code": "401"
            })
    
    if isInvalidVerificationCode(verification_code):
        return verificationFailedJson()
    
    user = getUserFromVerificationCode(verification_code)
    user.validate_status = 1
    user.validate_time = datetime.now()
    user.save()
    return JsonResponse({
                "message": "Email successfully verified.",
                "http_code": "200"
            })

def GetAdminUsersView(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = CustomUser.objects.filter(admin = 1).values()
    return JsonResponse({
                "data": [user['id'] for user in data],
                "http_code": "200"
            })

def GetUnvalidatedUsersView(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = CustomUser.objects.filter(validate_status = 0).values()
    return JsonResponse({
                "data": [user['id'] for user in data],
                "http_code": "200"
            })
def CreateSubCategoryView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    params = ["name", "user_id"]
    validated_params = [param in data for param in params]
    if not all(validated_params):
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "401"
        })
    name = data['name']
    user_id = data['user_id']
    if type(user_id) != int:
        return JsonResponse({
                "message": "Please enter a valid user id",
                "http_code": 401
            })
    user = getUserById(user_id)
    subcategory = SubCategory(name = name, user_id = user)
    subcategory.save()
    obj = model_to_dict(subcategory)
    return JsonResponse({
                "data": obj,
                "http_code": "201"
            })

def GetSubCategoriesView(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    user_id = data['user_id']
    result = SubCategory.objects.filter(user_id = user_id).values()
    return JsonResponse({
                "data": list(result),
                "http_code": "200"
            })

def DeleteSubCategoryView(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "GET"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    subCategoryID = data['subCategoryID']
    SubCategory.objects.filter(id = subCategoryID).delete()
    return JsonResponse({
                "http_code": "204"
            })

def CreateOrderView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    params = ["buyer_id", "seller_id", "item_id", "quantity", "status", 'txid']
    validated_params = [param in data for param in params]
    if not all(validated_params):
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "401"
        })
    
    buyer_id = getUserById(data['buyer_id'])
    seller_id = getUserById(data['seller_id'])
    item_id = getItemById(data['item_id'])
    quantity = data['quantity']
    status = data['status']
    transaction_id = data['txid']
    
    txid = Transaction(transaction_id)
    txid.save()
    if buyer_id == seller_id:
        return JsonResponse({
                "message": "Buyer cannot be the seller",
                "http_code": "401"
            })
    
    order = Order(buyer_id = buyer_id, seller_id = seller_id, item_id = item_id, quantity = quantity, status = status, transaction_id = txid)
    order.save()
    print(order.id)
    return JsonResponse({
            "message": order.id,
            "http_code": 201
        })


def GetOrderView(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = request.GET
    params = ["id"]
    validated_params = [param in data for param in params]
    if not all(validated_params):
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "401"
        })
    
    order_id = data['id']
    result = Order.objects.filter(id = order_id).values()
    return JsonResponse({
                "data": list(result),
                "http_code": "200"
            })

def GetOrdersOfBuyer(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = request.GET
    params = ["id"]
    validated_params = [param in data for param in params]
    if not all(validated_params):
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "401"
        })
    
    buyer_id = data['id']
    result = Order.objects.filter(buyer_id = buyer_id).values()
    return JsonResponse({
                "data": list(result),
                "http_code": "200"
            })

def GetOrdersOfSeller(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = request.GET
    params = ["id"]
    validated_params = [param in data for param in params]
    if not all(validated_params):
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "401"
        })
    
    seller_id = data['id']
    result = Order.objects.filter(buyer_id = seller_id).values()
    return JsonResponse({
                "data": list(result),
                "http_code": "200"
            })
    
def CreateItemView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    params = ["category", "name", "price", "stock", "description", 'discount', "subcategory_id", "user_id"]
    validated_params = [param in data for param in params]
    if not all(validated_params):
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "401"
        })
    
    category = data['category']
    name = data['name']
    price = data['price']
    stock = data['stock']
    desc = data['description']
    discount = data['discount']
    subcategory_id = getSubCategoryFromId(data['subcategory_id'])
    user_id = getUserById(data['user_id'])
    image = ""
    
    item = Item(category = category, name = name, image = image, price = price, stock = stock, description = desc, discount = discount, subcategory_id = subcategory_id, user_id = user_id)
    item.save()
    return JsonResponse({
            "data": item.id,
            "http_code": "201"
        })

def UpdateItemView(request):
    if checkInvalidRoutes(request.method, ["GET", "POST", "DELETE"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    item_id = data['item_id']
    category = data['category'] or None
    name = data['name'] or None
    price = data['price'] or None
    stock = data['stock'] or None
    desc = data['description'] or None
    discount = data['discount'] or None
    subcategory_id = data['subcategory_id'] or None
    
    item_list = Item.objects.filter(id = item_id)
    if not item_list:
        return JsonResponse({
            "message": "Item not found",
            "http_code": "404"
        })
    item = item_list[0]
    if category: item.category = category
    if name: item.name = name
    if price: item.price = price
    if stock: item.stock = stock
    if desc: item.desc = desc
    if discount: item.discount = discount
    if subcategory_id: item.subcategory_id = subcategory_id
    item.save()
    return JsonResponse({
        "data": item,
        "http_code": "200"
    })

def GetItemView(request):
    if checkInvalidRoutes(request.method, ["PUT", "POST", "DELETE"]):
        return handleInvalidRouteJson()
    data = request.GET
    params = ["item_id"]
    validated_params = [param in data for param in params]
    if not all(validated_params) or type(data['item_id']) != int:
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "401"
        })
    item_id = data['item_id']
    item_list = Item.objects.filter(id = item_id)
    if not item_list:
        return JsonResponse({
            "message": "Item not found",
            "http_code": "404"
        })
    item = item_list[0]
    return JsonResponse({
        "data": item.id,
        "http_code": "200"
    })

def DeleteItemView(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "GET"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    params = ["item_id"]
    validated_params = [param in data for param in params]
    if not all(validated_params) or type(data['item_id']) != int:
        return JsonResponse({
            "message": "Invalid params",
            "http_code": "401"
        })
    item_id = data['item_id']
    filtered_item = Item.objects.filter(id = item_id)
    if not filtered_item:
        return JsonResponse({
                "message": "Item not found",
                "http_code": "404"
            })
    filtered_item.delete()
    return JsonResponse({
            "http_code": "204"
    })
    
def TransferTokens(request):
    """
    :description: Transfer DANC tokens from sender wallet to receiver wallet
    :param request: http post request. Body contains sender email, receiver email, and amount
    :return: http response with transaction hash
    """

    # only allow POST request
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()

    data = json.loads(request.body)
    senderEmail = data['senderEmail']
    receiverEmail = data['receiverEmail']
    amount = data['amount']

    # check if sender and receiver exists
    if not checkIfUserExists(senderEmail):
        return JsonResponse({
            "message": "Sender does not exist",
            "http_code": "404"
        })
    if not checkIfUserExists(receiverEmail):
        return JsonResponse({
            "message": "Receiver does not exist",
            "http_code": "404"
        })

    sender = getUser(senderEmail)
    sender_address = sender.wallet.address
    sender_key = sender.wallet.private_key

    receiver = getUser(receiverEmail)
    receiver_address = receiver.wallet.address

    # send transaction to ethereum network
    tx_hash = transfer(sender_address, sender_key, receiver_address, amount)

    return JsonResponse({
        "message": f"{tx_hash.hex()}",
        "http_code": "200"
    })