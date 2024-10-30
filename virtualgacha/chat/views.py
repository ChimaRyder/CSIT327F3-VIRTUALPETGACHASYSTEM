from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ChatRoom, Message

# Create your views here.
def chat_view(request):
    return render(request, 'chat/chatbox.html')

def message_list(request):
    try:
        room = ChatRoom.objects.get(name='Global Chat')
        messages = room.messages.all().order_by('timestamp')
        message_list = []
        for message in messages:
            message_list.append({
                'sender': message.sender.username,
                'content': message.content,
                #'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M')
                'timestamp': message.timestamp.strftime('%I:%M %p')
            })
        return JsonResponse(message_list, safe=False)
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Chat room not found.'}, status=404)