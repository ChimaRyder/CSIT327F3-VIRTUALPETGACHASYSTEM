from django import forms
from .models import Transaction, GCashDetails, CardDetails

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user_id', 'amount', 'status', 'payment_method']

class GCashDetailsForm(forms.ModelForm):
    class Meta:
        model = GCashDetails
        fields = ['gcash_number', 'receiver_name', 'reference_number']

class CardDetailsForm(forms.ModelForm):
    class Meta:
        model = CardDetails
        fields = ['card_number', 'card_name', 'card_expiry_date', 'card_security_code']