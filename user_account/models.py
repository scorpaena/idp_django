from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'SuperAdmin'),
        ('companyadmin', 'CompanyAdmin'),
        ('participant', 'Participant'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    company = models.ForeignKey('company.Company', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username
