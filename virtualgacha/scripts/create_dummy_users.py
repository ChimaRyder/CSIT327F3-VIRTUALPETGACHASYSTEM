import os
import django
import random
from django.contrib.auth.models import User
from faker import Faker
from login_register.models import Profile

fake = Faker()

def get_random_avatar():
    avatars = ['avatar1.png', 'avatar2.png', 'avatar3.png', 'avatar4.png']
    return random.choice(avatars)

def create_dummy_users(num_users=50):
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthdate = fake.date_of_birth()

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        profile = Profile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            total_credits=500,
            avatar=get_random_avatar()
        )

        print(f"Created user: {username} with profile: {profile}")

# Example usage
def run(*args):
    create_dummy_users(50)