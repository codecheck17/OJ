import email
from django.db import models

# Create your models here.
class MyUser(models.Model):
    user_name = models.CharField(max_length=50)
    email_id = models.EmailField()
    def __str__(self):
        return self.user_name
