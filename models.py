from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now 

class Machine(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

class Calibration(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
    ]

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    date = models.DateField()
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')

    def __str__(self):
        return f"{self.machine.name} - {self.status}"
