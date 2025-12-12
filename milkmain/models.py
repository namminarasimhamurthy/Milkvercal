from django.db import models

class MilkUser(models.Model):
    SHIFT_CHOICES = (
        ('morning', 'Morning'),
        ('evening', 'Evening'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    quality = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # <-- added

    def __str__(self):
        return f"{self.name} ({self.shift})"

class DailyRecord(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('unpaid', 'Unpaid')
    ]
    
    user = models.ForeignKey(MilkUser, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    milk_quantity = models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    def __str__(self):
        return f"{self.user.name} - {self.milk_quantity}L - ₹{self.amount} on {self.date} ({self.status})"
