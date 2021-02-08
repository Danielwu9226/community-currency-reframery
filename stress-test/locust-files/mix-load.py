from locust import HttpUser, TaskSet, task, between
import json
import string
import random

USER_CREDENTIALS = [
    ("u1", "password"),
    ("u2", "password"),
    ("u3", "password"),
    ("u4", "password"),
    ("u5", "password"),
    ("u6", "password"),
    ("u7", "password"),
    ("u8", "password"),
    ("u9", "password"),
    ("u10", "password"),
    ("u11", "password"),
    ("u12", "password"),
    ("u13", "password"),
    ("u14", "password"),
    ("u15", "password"),
    ("u16", "password"),
    ("u17", "password"),
    ("u18", "password"),
    ("u19", "password"),
    ("u20", "password"),
    ("u21", "password"),
    ("u22", "password"),
    ("u23", "password"),
    ("u24", "password"),
    ("u25", "password"),
    ("u26", "password"),
    ("u27", "password"),
    ("u28", "password"),
    ("u29", "password"),
    ("u30", "password"),
    ("u31", "password"),
    ("u32", "password"),
    ("u33", "password"),
    ("u34", "password"),
    ("u35", "password"),
    ("u36", "password"),
    ("u37", "password"),
    ("u38", "password"),
    ("u39", "password"),
    ("u40", "password"),
    ("u41", "password"),
    ("u42", "password"),
    ("u43", "password"),
    ("u44", "password"),
    ("u45", "password"),
    ("u46", "password"),
    ("u47", "password"),
    ("u48", "password"),
    ("u49", "password"),
    ("u50", "password"),
    ("u51", "password"),
    ("u52", "password"),
    ("u53", "password"),
    ("u54", "password"),
    ("u55", "password"),
    ("u56", "password"),
    ("u57", "password"),
    ("u58", "password"),
    ("u59", "password"),
    ("u60", "password"),
    ("u61", "password"),
    ("u62", "password"),
    ("u63", "password"),
    ("u64", "password"),
    ("u65", "password"),
    ("u66", "password"),
    ("u67", "password"),
    ("u68", "password"),
    ("u69", "password"),
    ("u70", "password"),
    ("u71", "password"),
    ("u72", "password"),
    ("u73", "password"),
    ("u74", "password"),
    ("u75", "password"),
    ("u76", "password"),
    ("u77", "password"),
    ("u78", "password"),
    ("u79", "password"),
    ("u80", "password"),
    ("u81", "password"),
    ("u82", "password"),
    ("u83", "password"),
    ("u84", "password"),
    ("u85", "password"),
    ("u86", "password"),
    ("u87", "password"),
    ("u88", "password"),
    ("u89", "password"),
    ("u90", "password"),
    ("u91", "password"),
    ("u92", "password"),
    ("u93", "password"),
    ("u94", "password"),
    ("u95", "password"),
    ("u96", "password"),
    ("u97", "password"),
    ("u98", "password"),
    ("u99", "password"),
]


class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task 
    def register(self):
        email = ''.join((''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),'@email.com'))
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        print({"email": email, "password": password})
        print(self.client.post('/register/', json={"email": email, "password": password}).content)

    @task
    def loginPathGetItem(self):
        if len(USER_CREDENTIALS) > 0:
            email, password = USER_CREDENTIALS.pop()
        print({"email": email, "password": password})
        response = self.client.post('/login/', json={"email": email, "password": password})
        response_string = response.content.decode('utf-8')
        user_id = (json.loads(response_string))['user_id']
        
        response = self.client.post('/getItem', json={"item_id": 1})

    @task
    def loginCreateDeleteSubcategory(self):
        if len(USER_CREDENTIALS) > 0:
            email, password = USER_CREDENTIALS.pop()
        print({"email": email, "password": password})
        response = self.client.post('/login/', json={"email": email, "password": password})
        response_string = response.content.decode('utf-8')
        user_id = (json.loads(response_string))['user_id']
        
        response = self.client.post('/createSubCategory', json={"name": "Product", "user_id": user_id})
        response_string = response.content.decode('utf-8')
        subcategory_id = (json.loads(response_string))['data']

        self.client.post('/deleteSubCategory', json={"subCategoryID": subcategory_id})

        self.client.post('/getItem', json={"item_id": 1})
