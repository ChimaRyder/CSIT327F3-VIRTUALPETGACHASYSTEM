from django.db import models
from django.contrib.auth.models import User
from inventory.models import Inventory
from django.db.models.signals import post_save
from django.dispatch import receiver
from daily_rewards.models import *
import random

BUILT_IN_AVATARS = [
    'avatar1.png',
    'avatar2.png',
    'avatar3.png',
    'avatar4.png',
]

def get_random_avatar():
    return random.choice(BUILT_IN_AVATARS)

def upload_to(i, filename):
    return f'uploaded_avatars/{i.user.id}/{filename}'

# Create your models here.
class Profile(models.Model):
    AVATAR_CHOICES = [
        ('avatar1.png', 'Avatar 1'),
        ('avatar2.png', 'Avatar 2'),
        ('avatar3.png', 'Avatar 3'),
        ('avatar4.png', 'Avatar 4'),
    ]

    # print(Reward.objects.latest('id'))



    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField(null=True, blank=True)
    total_credits = models.IntegerField(default=500)
    avatar = models.CharField(max_length=50, default=get_random_avatar, blank=True, null=True)
    uploaded_avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)
    following = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)
    showcased_pets = models.ManyToManyField(Inventory, blank=True, related_name="showcased_by")

    def get_profile_image_url(self):
        if self.uploaded_avatar:
            return self.uploaded_avatar.url
        elif self.avatar:
            return f'/media/avatars/{self.avatar}'
        return '/media/avatars/avatar1.png'
    
    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.title()
        if self.last_name:
            self.last_name = self.last_name.title()
        
        if self.user.first_name != self.first_name or self.user.last_name != self.last_name:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.save()

        super().save(*args, **kwargs)


    def __str__(self):
        return self.user.username
