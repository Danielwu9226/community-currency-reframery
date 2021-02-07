from django.http import JsonResponse
import json 
from reframery.models import CustomUser, SubCategory, Order, Item, Wallet
from reframery.services.ethService import generate_eth_account, transfer
from datetime import datetime


# Create your views here.

def checkInvalidRoutes(method, route_list):
    return method in route_list


def handleInvalidRouteJson():
    return JsonResponse({
        "message": "Invalid Route",
        "http_code": "401 Unauthorized"
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

def getUserById(user_id):
    return CustomUser.objects.filter(id = user_id)[0]

def isInvalidVerificationCode(verification_code):
    return len(CustomUser.objects.filter(validate_code=verification_code)) != 1


def getUserFromVerificationCode(verification_code):
    return CustomUser.objects.filter(validate_code=verification_code)[0]


def RegisterView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()

    data = json.loads(request.body)
    email = data['email']
    password = data['password']

    if checkIfUserExists(email):
        return JsonResponse({
            "message": "User already exists.",
            "http_code": "404"
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

    # TODO:
    # sendVerificationEmail(email, verification_code)

    return JsonResponse({
        "message": "User successfully created.",
        "http_code": "200",
        "jwt": user.token()
    })


def LoginView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()

    data = json.loads(request.body)
    email = data['email']
    password = data['password']
    if not checkIfUserExists(email):
        return authFailedJson()
    user = getUser(email)
    if not user.check_password(password):
        return authFailedJson()

    return JsonResponse({"jwt": user.token()})


def ForgotPasswordView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()

    data = json.loads(request.body)
    email = data['email']
    password = data['password']
    if not checkIfUserExists(email):
        return authFailedJson()
    user = getUser(email)
    user.set_password(password)
    user.save()
    return JsonResponse({
        "message": "Password successfully changed.",
        "http_code": "200"
    })


def EmailConfirmationView(request, verification_code):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
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
    data = list(CustomUser.objects.filter(admin = 1))
    return JsonResponse({
                "data": data,
                "http_code": "200"
            })

def GetUnvalidatedUsersView(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = list(CustomUser.objects.filter(validate_status = 0))
    return JsonResponse({
                "data": data,
                "http_code": "200"
            })
def CreateSubCategoryView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    name = data['name']
    user_id = data['user_id']
    user = getUserById(user_id)
    subcategory = SubCategory(name = name, user_id = user)
    subcategory.save()
    return JsonResponse({
                "data": {"name": subcategory.name},
                "http_code": "201"
            })

def GetSubCategoriesView(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    user_id = data['user_id']
    result = list(SubCategory.objects.filter(user_id = user_id))
    return JsonResponse({
                "data": result,
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

#TODO: 
def CreateOrderView(request):
    pass

#TODO: 
def UpdateOrderView(request):
    pass

def GetOrderView(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    order_id = data['id']
    result = list(Order.objects.filter(id = order_id))
    return JsonResponse({
                "data": result,
                "http_code": "200"
            })
#TODO:
def GetOrdersOfBuyer(request):
    pass

#TODO:
def GetOrdersOfSeller(request):
    pass
    
def CreateItemView(request):
    if checkInvalidRoutes(request.method, ["GET", "PUT", "DELETE"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    category = data['category']
    name = data['name']
    price = data['price']
    stock = data['stock']
    desc = data['description']
    discount = data['discount']
    subcategory_id = data['subcategory_id']
    user_id = data['user_id']
    image = ""
    
    item = Item(category, name, image, price, stock, desc, discount, subcategory_id, user_id)
    item.save()
    return JsonResponse({
            "data": item,
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
    data = json.loads(request.body)
    item_id = data['item_id']
    item_list = Item.objects.filter(id = item_id)
    if not item_list:
        return JsonResponse({
            "message": "Item not found",
            "http_code": "404"
        })
    item = item_list[0]
    return JsonResponse({
        "data": item,
        "http_code": "200"
    })

def DeleteItemView(request):
    if checkInvalidRoutes(request.method, ["POST", "PUT", "GET"]):
        return handleInvalidRouteJson()
    data = json.loads(request.body)
    item_id = data['item_id']
    Item.objects.filter(id = item_id).delete()
    return JsonResponse({
            "http_code": "204"
    })
    
def TransferTokens(request):
    """
    :description: Transfer DANC tokens from sender wallet to receiver wallet
    :param request: http post request. Body contains sender email, receiver email, and amount
    :return: http response with transaction hash
    """
    # TODO: JWT TOKEN

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