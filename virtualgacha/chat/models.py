from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatRoom(models.Model):
    ROOM_TYPES = [
        ('global', 'Global'),
        ('private', 'Private')
    ]

    type = models.CharField(max_length=10, choices=ROOM_TYPES)
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]} at {self.timestamp}"
