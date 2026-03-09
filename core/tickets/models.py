from django.db import models

class Ticket(models.Model):
    SERVICE_CHOICES = [
        ('survey', 'Survey Request'),
        ('maps', 'Map Request'),
        ('info', 'Information Request'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service}"


