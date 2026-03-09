from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
User = get_user_model()



# Audit Log Model (Put FIRST)

class AuditLog(models.Model):

    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('CHECKOUT', 'Checkout'),
        ('DELETE', 'Delete'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)

    visitor = models.ForeignKey(
        'Visitor',
        on_delete=models.CASCADE
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    description = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action}"



# User Profile Model


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('REGISTRATION_OFFICER', 'Registration Officer'),
        ('SUPERVISOR', 'Supervisor'),
        ('ADMIN', 'Administrator'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    department = models.ForeignKey(
        'Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# Department Model


class Department(models.Model):

    CORE = 'CORE'
    SUPPORT = 'SUPPORT'

    CATEGORY_CHOICES = [
        (CORE, 'Core Department'),
        (SUPPORT, 'Support Service'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name



# Purpose Model


class Purpose(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Contact must be exactly 10 digits."
)

id_validator = RegexValidator(
    regex=r'^\d{8}$',
    message="ID number must be exactly 8 digits."
)


# Visitor Model


class Visitor(models.Model):

    VISITOR_TYPE_CHOICES = [
        ('CITIZEN', 'Citizen'),
        ('CONTRACTOR', 'Contractor'),
        ('GOV_OFFICIAL', 'Government Official'),
        ('VISITOR', 'Visitor'),
    ]

    full_name = models.CharField(max_length=200)
    id_number = models.CharField(
    max_length=8,
    validators=[id_validator]
)
    contact = models.CharField(
    max_length=10,
    validators=[phone_validator]
)
    visitor_type = models.CharField(
        max_length=50,
        choices=VISITOR_TYPE_CHOICES,
        default='VISITOR'
    )

    organization = models.CharField(max_length=200, blank=True, null=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
 
    purpose = models.ForeignKey(
        Purpose,
        on_delete=models.CASCADE
    )

    expected_duration = models.CharField(max_length=50)
    items_carried = models.TextField(blank=True, null=True)

    check_in_time = models.DateTimeField(auto_now_add=True)

    check_out_time = models.DateTimeField(blank=True, null=True)

    checked_out = models.BooleanField(default=False)


    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_visitors"
    )

    checked_out_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='performed_checkouts'
    )

    class Meta:
        indexes = [
            models.Index(fields=['check_in_time']),
            models.Index(fields=['checked_out']),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.id_number}"


    # Checkout Logic (Audit Logging Included)

    def checkout(self, user):

        if self.checked_out:
            raise ValueError("Visitor already checked out")

        now = timezone.now()

        if self.check_in_time and now <= self.check_in_time:
            now = self.check_in_time + timedelta(seconds=1)

        self.check_out_time = now
        self.checked_out = True
        self.checked_out_by = user
        self.save()

    #  CREATE AUDIT LOG
        AuditLog.objects.create(
        user=user,
        action='CHECKOUT',
        visitor=self,
        description=f"{user} checked out visitor {self.full_name}"
    )
    @property
    def duration_inside(self):
        if self.checked_out and self.check_out_time:
           return self.check_out_time - self.check_in_time
        else:
         return timezone.now() - self.check_in_time

      