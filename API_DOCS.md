# DANC Backend API Documentation and README

How to use Postman to test the API:

After installing all the dependencies, do the following steps:

https://www.postman.com/
Run the server with: python manage.py runserver

For the /register function, in postman follow the screenshot:

 



/register:
```
Register: /register
Methods allowed: [POST]
Params Required: Json Object of {
                    email: String
                    password: String
                 }
Exceptions: [UserAlreadyExists]
Return: JsonResponse({
            "message": "User successfully created.",
            "http_code": "200",
            "jwt": user.token
        })
```
/login:
```
Login: /login
Methods allowed: [POST]
Params Required: Json Object of {
                    email: String
                    password: String
                 }
Exceptions: [UserDoesNotExist, PasswordIncorrect]
Return: JsonResponse({
            "jwt": user.token
        })
```

/forgotpassword
```
Forgot Password: /forgotpassword
Methods allowed: [POST]
Params Required: Json Object of {
                    email: String
                    password: String
                 }
Exceptions: [UserDoesNotExist]
Return: JsonResponse({
            "message": "Password successfully changed.",
            "http_code": "200"
        })
```

/verify/<verification_code>
```
Email Confirmation: /verify/<verification_code>
Methods allowed: [POST]
Params Required: None
Exceptions: None
Return: JsonResponse({
                "message": "Email successfully verified.",
                "http_code": "200"
        })
```

/getAdminUsers
```
Get Admin Users: /getAdminUsers
Methods allowed: [GET]
Params Required: None
Exceptions: None
Return: JsonResponse({
                data: [AdminUsers],
                "http_code": "200"
        })
```

/getUnvalidatedUsers
```
Get Unvalidated Users: /getUnvalidatedUsers
Methods allowed: [GET]
Params Required: None
Exceptions: None
Return: JsonResponse({
                data: [UnvalidatedUsers],
                "http_code": "200"
        })
```


/createSubCategory
```
    Description: create the subcateogry
    Methods allowed: [POST]
    Params Required: Json Object of{
                name: String
                user_id: String
                }
    Exceptions: None
    Return: JsonResponse({
                data: [name],
                "http_code": "201"
        })
```

/getSubCategories
```
Description: get the subcategory
Methods allowed: [GET]
Params Required: Json Object of {
        user_id: String
        }
Exceptions: None
Return: JsonResponse({
            data: [result],
            "http_code": "200"
    })

```

/deleteSubCategory
```
Description: delete the subcategory
Methods allowed: [DELETE]
Params Required: Json Object of {
        subCategoryID: String
        }
Exceptions: None
Return: JsonResponse({
            "http_code": "204"
    })
```


/getOrder
```
Description: get the order
Methods allowed: [GET]
Params Required: Json Object of {
        order_id: String
        }
Exceptions: None
Return: JsonResponse({
            data: [result],
            "http_code": "200"
    })
```

/createItem
```
CreateItem : /createItem
Methods allowed: [POST]
Params require: Json Object of {
    category : string
    name : string
    price : string
    stock : string
    desc : string
    discount : string
    subcategory_id : string
    user_id : string 
    image : string
}
Exceptions: None
Return: JsonResponse({
        "data" : item
        "http_code": "200"
        })
```

/updateItem
```
UpdateItem: /updateItem
Methods allowed: [PUT]
Params Required: Json Object of {
                        item_id : string
                        category : string
                        name : string
                        price : string
                        stock : string
                        desc : string
                        discount : string
                        subcategory_id : string
                        }

Exceptions: [Item not Found]
Return JsonResponse({
            "message" : "Item not found",
            "http_code": "404"

})
```

/getItem
```
Get Item: /getItem
Methods allowed: [GET]
Params Required: Json Object of {
                    item_id : string
                    }
Exceptions: [ItemNotFound]
                Return: JsonResponse({
                            "message": "Item not found",
                            "http_code": "404"
                })
Return: JsonResponse({
                    "data" : item,
                    "http_code": "200"

})
```

/deleteItem
```
Delete Item: /DeleteItem
Methods allowed: [DELETE]
Params Required:  Json Object of {
                    item_id : string
                    }
Exceptions: None
Return: JsonResponse({
                "http_code": "204"
})
```

















