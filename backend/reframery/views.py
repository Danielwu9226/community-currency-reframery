from django.http import JsonResponse
import json 
from reframery.models import CustomUser, SubCategory, Order, Item
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
    return len(CustomUser.objects.filter(email = email)) == 1

def getUser(email):
    return CustomUser.objects.filter(email = email)[0]

def isInvalidVerificationCode(verification_code):
    return len(CustomUser.objects.filter(validate_code = verification_code)) != 1

def getUserFromVerificationCode(verification_code):
    return CustomUser.objects.filter(validate_code = verification_code)[0]

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
    
    verification_code = user.validate_code
    
    #TODO:
    #sendVerificationEmail(email, verification_code)
    
    return JsonResponse({
                "message": "User successfully created.",
                "http_code": "200"
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
    
    #TODO: RETURN JWT TOKEN
    return JsonResponse({"blah":"blah"})

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
    subcategory = SubCategory(name, user_id)
    subcategory.save()
    return JsonResponse({
                "data": subcategory,
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
    
