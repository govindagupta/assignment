from django.db import models

# Create your models here.

class Account(models.Model):
    """
    Information about User Account
    """
    auth_id = models.CharField(max_length=32)
    username = models.CharField(max_length=32)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'account'

class PhoneNumber(models.Model):
    """
    Information about a Phone number registered against account
    """
    number = models.CharField(max_length=16)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

    class Meta:
        db_table = 'phone_number'
