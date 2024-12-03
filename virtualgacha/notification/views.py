from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from login_register.models import Profile
from notification.models import Notification


# Create your views here.
def notification_page(request):
    profile = Profile.objects.get(user=request.user)
    items_per_page = 5
    notifications = Notification.objects.filter(user=request.user)
    notifications = notifications.order_by("notif_status").order_by("created_at").reverse()

    if request.GET:
        notif = Notification.objects.get(id=request.GET.get('notif-read'))
        if notif.notif_status == Notification.Status.unread:
            notif.notif_status = Notification.Status.read
            notif.save()
        return redirect(notif.link)

    if request.method == "POST" and request.POST["notif-claimed"]:
        notif = Notification.objects.get(id=request.POST.get("notif-claimed"))
        profile.total_credits += notif.claim_coins
        notif.claim_coins = 0
        notif.notif_status = Notification.Status.read
        notif.save()
        profile.save()

    paginator = Paginator(notifications, items_per_page)
    page = request.GET.get('page', 1)
    notifications = paginator.get_page(page)

    return render(request, "notification_page.html", {'profile': profile, "notifications_list": notifications})

