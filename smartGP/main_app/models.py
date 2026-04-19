from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username

# Create your models here.
class Complaint(models.Model):
    COMPLAINT_CATEGORIES = [
        ('road', 'Damaged Roads'),
        ('electricity', 'Electricity Issues'),
        ('water', 'Water Supply Problems'),
        ('waste', 'Garbage & Sanitation'),
        ('health', 'Health & Medical Facilities'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_CATEGORIES)
    description = models.TextField()
    image = models.ImageField(upload_to='complaints/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.get_complaint_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"
    
class SchemeApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  
    name = models.CharField(max_length=255)
    aadhaar = models.CharField(max_length=12, unique=False)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    address = models.TextField()
    scheme = models.CharField(max_length=255)  # Stores the scheme name
    income = models.PositiveIntegerField()
   
    documents = models.FileField(upload_to='documents/', blank=True, null=True)  # File upload
    is_approved = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.name} - {self.scheme}"
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title