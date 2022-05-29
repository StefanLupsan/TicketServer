from django.db import models
from scripts.GenerateTokens import generate_qr_link
# Create your models here.


class PromTicket(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    age = models.IntegerField(default=0)
    qr_link = models.CharField(unique=True, max_length=400, default=generate_qr_link)
    is_valid = models.IntegerField(default=1)
    mail_sent = models.IntegerField(default=0)


class AfterTicket(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    age = models.IntegerField(default=0)
    qr_link = models.CharField(unique=True, max_length=400, default=generate_qr_link)
    is_valid = models.IntegerField(default=1)
    mail_sent = models.IntegerField(default=0)
