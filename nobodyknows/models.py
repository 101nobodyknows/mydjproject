from django.db import models

class user_contact_review(models.Model):
    name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    subject = models.CharField(max_length = 60)
    message = models.TextField()