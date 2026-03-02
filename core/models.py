from django.db import models

# Create your models here.
# core/models.py
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    posted_on = models.DateField(auto_now_add=True)
    salary = models.CharField(max_length=100,blank=True,null=True)
    required_skills = models.TextField()

    def __str__(self):
        return self.title

class Internship(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    stipend = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    skills = models.TextField() 
    def __str__(self):
        return self.title

