from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']
