from faker import Faker
import json

from locust import  TaskSet, task,FastHttpUser,constant


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


class WebsiteUser(FastHttpUser):
    tasks = [UserBehavior]
    wait_time = constant(0.4)