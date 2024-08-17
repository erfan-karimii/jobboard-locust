import jwt
import datetime
import os
import django

# Set up Django environment to access models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_django_project.settings")
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model

# Get the Django SECRET_KEY
SECRET_KEY = settings.SECRET_KEY

# Define a function to generate JWT
def create_jwt_for_user(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }

    # Create JWT using Django's SECRET_KEY
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Example usage
if __name__ == "__main__":
    # Fetch a user from Django's database
    User = get_user_model()
    user = User.objects.get(username="testuser")  # Replace with your actual username or filter condition

    # Generate JWT for the user
    token = create_jwt_for_user(user)
    print("Generated JWT:", token)
