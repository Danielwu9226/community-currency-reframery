from django.http import JsonResponse
import json 
from reframery.models import CustomUser
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