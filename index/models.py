from django.db import models
from django.contrib.auth.models import User
# Create your models here.
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