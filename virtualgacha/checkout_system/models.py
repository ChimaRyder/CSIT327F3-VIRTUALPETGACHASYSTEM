from django.db import models

class GCashDetails(models.Model):
    gcash_number = models.CharField(max_length=11)
    receiver_name = models.CharField(max_length=100)
    reference_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"GCash {self.gcash_number} - {self.receiver_name}"

class CardDetails(models.Model):
    card_number = models.CharField(max_length=16)
    card_name = models.CharField(max_length=100)
    card_expiry_date = models.CharField(max_length=5)
    card_security_code = models.CharField(max_length=4)

    def __str__(self):
        return f"Card {self.card_number} - {self.card_name}"

class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('GCASH', 'GCash'),
        ('CARD', 'Card'),
    ]

    TRANSACTION_TYPE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    STATUS_CHOICES = [
        ('WAITING', 'Waiting'),
        ('SUCCESS', 'Success'),
        ('DECLINED', 'Declined'),
    ]
    transaction_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    credits_amount = models.FloatField(default=0.0)
    total_changes = models.FloatField(default=0.0)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, default='BUY')
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,  choices=STATUS_CHOICES, default='WAITING')
    payment_method = models.CharField(max_length=5, choices=PAYMENT_METHOD_CHOICES)
    gcash_details = models.ForeignKey(GCashDetails, on_delete=models.CASCADE, blank=True, null=True)
    card_details = models.ForeignKey(CardDetails, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"