from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	Sex_choise = ((0,"Male"),(1,"Female"),(2,"Other"))
	code = models.CharField(max_length=12)
	DOB = models.DateTimeField(blank=True, null=True)
	PhoneNumber = models.IntegerField(blank=True, null=True)
	Sex = models.IntegerField(blank=True, null=True, choices= Sex_choise)
	Active = models.BooleanField(default=False)
class Category(models.Model):
	UserID = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	Name = models.CharField(max_length=100)
	Description = models.TextField()
	Is_Extention = models.BooleanField()
class Vocabulary(models.Model):
	CategoryID = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)
	Term = models.CharField(max_length=100)
	Definition = models.TextField()
	Tick = models.BooleanField(default=False)
	Mark = models.IntegerField(blank=True)
	Date = models.DateTimeField(auto_now_add=True)
class Dictionary(models.Model):
	Term = models.CharField(max_length=100)
class Definition(models.Model):
	Dictionary = models.ForeignKey(Dictionary, default=None, on_delete=models.CASCADE)
	Definition = models.CharField(max_length=100)
class Contacts(models.Model):
	FirstName = models.CharField(max_length=100)
	LastName = models.CharField(max_length=100)
	Email = models.CharField(max_length=100)
	Messenger = models.TextField()