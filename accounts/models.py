from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin/Warden'),
        ('technician', 'Technician'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)

    # This field is required for the student role.
    # We keep it blank=True here so Admins/Technicians can register without it.
    roll_no = models.CharField(max_length=50, blank=True, null=True, help_text='Student roll number')

    def is_student(self):
        return self.role == 'student'

    def is_admin_role(self):
        return self.role == 'admin'

    def is_technician(self):
        return self.role == 'technician'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"