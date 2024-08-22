import json
import os
from random import randint , choice
from locust import TaskSet, task, FastHttpUser, constant
import requests
from faker import Faker
from decouple import config

fake = Faker()
HOST = config("HOST", default="http://192.168.1.79")
MAX_USER_ID = config("MAX_USER_ID", default=650000,cast=int)

def login_random_user():
    """
    this function send POST for login end point , recive jwt (access Token) and return proper header foor authenticatin
    """
    random_id = randint(1, MAX_USER_ID)
    payload = {"id": random_id}
    headers = {"content-type": "application/json"}
    try:
        response = requests.post(
            f"{HOST}/load_test/p_update/",
            data=json.dumps(payload),
            headers=headers,
        )
        access = response.json().get("access")
        if "notfound" == access:
            print("user not found")
        else:
            headers = {
                "content-type": "multipart/form-data",
                "Authorization": f"Bearer {access}",
            }

            return headers

    except Exception as e:
        print(f"Request failed: {e}")


class UserBehavior(TaskSet):
    @task(1)
    def create_user_load_test(self):
        email = str(fake.name()) + str(fake.city()) + str(fake.random_int())
        email_without_space = "".join(email.split())
        payload = {
            "email": f"{email_without_space}@gmail.com",
        }
        headers = {"content-type": "application/json"}
        try:
            response = self.client.post(
                "/account/user/login/", data=json.dumps(payload), headers=headers
            )
            print(response.text)
            response.raise_for_status()  # Raises an error for 4xx/5xx status codes
        except Exception as e:
            print(f"Request failed: {e}")


    @task(4)
    def update_profile_loadtest(self):
        headers = login_random_user()
        folder_path = "./images"
        
        # List files once and use choice for random selection
        files = os.listdir(folder_path)
        if not files:
            print("No files found in the folder.")
            return
        
        random_image = choice(files)  # More efficient random selection
        file_path = os.path.join(folder_path, random_image)  # Use os.path.join for better path handling
        
        data = {
            "fullname": str(fake.name()),
        }
        
        try:
            with open(file_path, "rb") as image_file:
                response = self.client.patch(
                    "/account/user/profile/", 
                    data=data, 
                    files={"resume_file": (os.path.basename(file_path), image_file, "image/jpeg")}, 
                    headers=headers
                )
                print(response.text)
                response.raise_for_status()
        except OSError as e:
            print(f"File operation failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    @task(8)
    def profile(self):
        """
        get User Profile --> Customer
        """

        headers = login_random_user()
        response  = self.client.get("/account/user/profile/", headers=headers)
        print(response.text)


class WebsiteUser(FastHttpUser):
    tasks = [UserBehavior]
    wait_time = constant(0.4)