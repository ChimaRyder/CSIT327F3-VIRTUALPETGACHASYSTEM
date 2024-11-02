from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Reward, UserReward
from datetime import date, timedelta
import calendar

@login_required
def daily_rewards(request):
    today = date.today()
    rewards = Reward.objects.filter(date__year=today.year, date__month=today.month)
    user_rewards = UserReward.objects.filter(user=request.user, reward__in=rewards)

    # Calculate streak
    streak = 0
    yesterday = today - timedelta(days=1)
    while UserReward.objects.filter(user=request.user, claim_date=yesterday, claimed=True).exists():
        streak += 1
        yesterday -= timedelta(days=1)

    # Check if the reward has been claimed today
    claimed_today = UserReward.objects.filter(user=request.user, reward__date=today, claimed=True).exists()
    if claimed_today:
        streak += 1

    # Calculate the number of days in the current month
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days = list(range(1, days_in_month + 1))

    # Calculate total claims
    total_claims = UserReward.objects.filter(user=request.user, claimed=True).count()

    # Create a list of tuples to map days to their claim status
    claim_status = []
    for day in days:
        if day > today.day:
            status = 'future'
        else:
            status = 'missed'
        for user_reward in user_rewards:
            if user_reward.reward.date.day == day:
                status = 'claimed' if user_reward.claimed else 'missed'
        claim_status.append((day, status))

    context = {
        'today': today,
        'rewards': rewards,
        'user_rewards': user_rewards,
        'streak': streak,
        'days': days,
        'total_claims': total_claims,
        'claimed_today': claimed_today,
        'claim_status': claim_status,
    }
    return render(request, 'daily_rewards_content.html', context)

@login_required
def claim_reward(request):
    today = date.today()
    reward = get_object_or_404(Reward, date=today)
    user_reward, created = UserReward.objects.get_or_create(user=request.user, reward=reward)
    if not user_reward.claimed:
        user_reward.claimed = True
        user_reward.claim_date = today
        user_reward.save()

        # Calculate streak
        streak = 0
        yesterday = today - timedelta(days=1)
        while UserReward.objects.filter(user=request.user, claim_date=yesterday, claimed=True).exists():
            streak += 1
            yesterday -= timedelta(days=1)
        streak += 1  # Include today's claim

        earned_credits = reward.credit_reward + streak  # Example: base reward credits + streak bonus
        request.session['earned_credits'] = earned_credits
        response_data = {'earned_credits': earned_credits}
        if reward.pet_reward:
            response_data['pet_reward'] = {
                'name': reward.pet_reward.pet_species,
                'rarity': reward.pet_reward.get_rarity_display(),
                'image_url': reward.pet_reward.pet_image.url
            }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Reward already claimed'}, status=400)