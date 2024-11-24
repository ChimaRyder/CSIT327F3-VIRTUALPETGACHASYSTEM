from notification.models import Notification


def notification_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, notif_status=Notification.Status.unread).count()
        return {'notifications': notifications}
    return {'notifications': 0}
