from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Transaction, GCashDetails, CardDetails
from login_register.models import Profile
from decimal import *

def process_transaction(request):
    print(request.POST)
    credits_amount = request.POST.get('amount')
    payment_method = request.POST.get('payment_method')
    total_changes = request.POST.get('total_changes')
    transaction_type = request.POST.get('transaction_type')

    print(request.user.profile.total_credits)

    # Update the total earnings for the user
    profile = Profile.objects.get(user=request.user)
    

    if transaction_type == 'BUY':
        profile.total_credits += int(credits_amount)
    else:
        if profile.total_credits < int(credits_amount):
            return JsonResponse({'status': 'FAILED', 'message': 'Insufficient credits'})
        else:
            profile.total_credits -= int(credits_amount)

    # Parse the total_changes value
    total_changes_value = float(total_changes.split('$')[1].replace(',', ''))

    transaction = Transaction(
        user_id=request.user.id,
        credits_amount=float(credits_amount),
        status="WAITING",
        payment_method=payment_method,
        total_changes=total_changes_value,
        transaction_type=transaction_type
    )

    if payment_method == 'GCASH':
        gcash_number = request.POST.get('gcash_number')
        receiver_name = request.POST.get('receiver_name')
        reference_number = request.POST.get('reference_number')
        gcash_details = GCashDetails(
            gcash_number=gcash_number,
            receiver_name=receiver_name,
            reference_number=reference_number
        )
        gcash_details.save()
        transaction.gcash_details = gcash_details
    elif payment_method == 'CARD':
        card_number = request.POST.get('card_number')
        card_name = request.POST.get('card_name')
        card_expiry_date = request.POST.get('card_expiry_date')
        card_security_code = request.POST.get('card_security_code')
        card_details = CardDetails(
            card_number=card_number,
            card_name=card_name,
            card_expiry_date=card_expiry_date,
            card_security_code=card_security_code
        )
        card_details.save()
        transaction.card_details = card_details

    transaction.save()
    response_data = {
        'transaction_type' : transaction.transaction_type,
        'status': 'SUCCESS',
        'transaction_id': transaction.transaction_id,
        'user_id': transaction.user_id,
        'amount': str(transaction.credits_amount),
        'total_changes': str(transaction.total_changes),
        'status_text': transaction.status,
        'payment_method': transaction.get_payment_method_display(),
    }
    if payment_method == 'GCASH':
        response_data.update({
            'gcash_number': transaction.gcash_details.gcash_number,
            'receiver_name': transaction.gcash_details.receiver_name,
            'reference_number': transaction.gcash_details.reference_number,
        })
    elif payment_method == 'CARD':
        response_data.update({
            'card_number': transaction.card_details.card_number,
            'card_name': transaction.card_details.card_name,
            'card_expiry_date': transaction.card_details.card_expiry_date,
            'card_security_code': transaction.card_details.card_security_code,
        })
    print("SUCCESS!")
    profile.save()
    return JsonResponse(response_data)

def checkout(request):
    profile = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        return process_transaction(request)
    return render(request, 'checkout_system_content.html', {'profile': profile})
