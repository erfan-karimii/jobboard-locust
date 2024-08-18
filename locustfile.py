import json
import requests
from random import randint
from faker import Faker
from locust import  TaskSet, task,FastHttpUser,constant
import os

fake = Faker()

class UserBehavior(TaskSet):
    @task
    def my_task(self):
        email = str(fake.name())+str(fake.city())+str(fake.random_int())
        email_without_space = ''.join(email.split())
        payload = {
            'email':f'{email_without_space}@gmail.com',
        }
        print(payload,'////////////////////////')
        headers = {'content-type': 'application/json'}
        try:
            response = self.client.post("/login/", data=json.dumps(payload), headers=headers)
            response.raise_for_status()  # Raises an error for 4xx/5xx status codes
        except Exception as e:
            print(f"Request failed: {e}")
    
    @task
    def update_profile_loadtest(self):
        random_id = 2
        payload = {
            'id': random_id
        }
        headers = {'content-type': 'application/json'}
        try:
            x = requests.post("http://127.0.0.1:8000/load_test/p_update/", data=json.dumps(payload), headers=headers)
            access = x.json().get("access")
            if "notfound"  == access:
                print("user not found")
            else:
                headers = {'content-type': 'multipart/form-data','Authorization':f'Bearer {access}'}
                
                
                folder_path = './images'
                files = os.listdir(folder_path)
                y = randint(0,len(files)-1)
                random_image = files[y]                
                resume_file = open(folder_path + '/' + random_image, 'rb')  
                file_path = folder_path + '/' + random_image
                data = {
                    "fullname" : str(fake.name()),
                }
                with open(file_path, 'rb') as image_file:
                    files = {
                        'resume_file': (os.path.basename(file_path), image_file, 'image/jpeg')
                    }
                
                    response = self.client.post("/profile/", data=data,files=files, headers=headers)
                    print(response.text)
                    response.raise_for_status()
                
        except Exception as e:
            print(f"Request failed: {e}")
        


class WebsiteUser(FastHttpUser):
    tasks = [UserBehavior]
    wait_time = constant(0.4)