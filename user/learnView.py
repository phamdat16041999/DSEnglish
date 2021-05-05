from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
import re
from index.models import Category, Vocabulary
from django.shortcuts import redirect
from django.db import connection


def learn(request, id):
	if request.user.is_authenticated:
		tick = Vocabulary.objects.filter(CategoryID_id=id, Tick = True)
		if(len(tick) == 0):
			newWord = {'newWord': Vocabulary.objects.filter(CategoryID_id=id), 'CategoryID_id' : id}
			return render(request, 'learn.html', newWord)
		else:
			newWord = {'newWord': tick, 'CategoryID_id' : id}
			return render(request, 'learn.html', newWord)
	else:
		return render(request, 'login.html')
def write(request, id):
	if request.user.is_authenticated:
		tick = Vocabulary.objects.filter(CategoryID_id=id, Tick = True)
		if(len(tick) == 0):
			newWord = {'newWord': Vocabulary.objects.filter(CategoryID_id=id), 'CategoryID_id' : id}
			return render(request, 'write.html', newWord)
		else:
			newWord = {'newWord': tick, 'CategoryID_id' : id}
			return render(request, 'write.html', newWord)			
	else:
		return render(request, 'login.html')
def speak(request, id):
	if request.user.is_authenticated:
		tick = Vocabulary.objects.filter(CategoryID_id=id, Tick = True)
		if(len(tick) == 0):
			newWord = {'newWord': Vocabulary.objects.filter(CategoryID_id=id), 'CategoryID_id' : id}
			return render(request, 'speak.html', newWord)
		else:
			newWord = {'newWord': tick, 'CategoryID_id' : id}
			return render(request, 'speak.html', newWord)
	else:
		return render(request, 'login.html')
def flipCard(request, id):
	if request.user.is_authenticated:
		tick = Vocabulary.objects.filter(CategoryID_id=id, Tick = True)
		if(len(tick) == 0):
			newWord = {'newWord': Vocabulary.objects.filter(CategoryID_id=id), 'CategoryID_id' : id}
			return render(request, 'flip card.html', newWord)
		else:
			newWord = {'newWord': tick, 'CategoryID_id' : id}
			return render(request, 'flip card.html', newWord)			
	else:
		return render(request, 'login.html')
def memoryCard(request, id):
	if request.user.is_authenticated:
		tick = Vocabulary.objects.filter(CategoryID_id=id, Tick = True)
		if(len(tick) == 0):
			newWord = {'newWord': Vocabulary.objects.filter(CategoryID_id=id), 'CategoryID_id' : id}
			return render(request, 'MemoryCard.html', newWord)
		else:
			newWord = {'newWord': tick, 'CategoryID_id' : id}
			return render(request, 'MemoryCard.html', newWord)			
	else:
		return render(request, 'login.html')
def plusPoints(request, Term, CategoryID_id):
	if request.user.is_authenticated:
		mark = Vocabulary.objects.all().get(Term = Term, CategoryID = CategoryID_id).Mark
		mark = int(mark)
		if mark <= 6:
			with connection.cursor() as cursor:
				cursor.execute(
				    "UPDATE index_vocabulary SET index_vocabulary.Mark = %s WHERE index_vocabulary.id = (SELECT index_vocabulary.id FROM index_vocabulary INNER JOIN index_category on index_vocabulary.CategoryID_id = index_category.id INNER JOIN index_user ON index_user.id = index_category.UserID_id WHERE index_user.id = '%s' AND index_vocabulary.Term = %s AND index_vocabulary.CategoryID_id = %s)" ,
				    [mark + 1, request.user.id, Term, CategoryID_id]
				)
			return render(request, 'learn.html') 
		else:
			return render(request, 'learn.html') 
	else:
		return render(request, 'login.html')
def subtractPoints(request, Term, CategoryID_id):
	if request.user.is_authenticated:
		mark = Vocabulary.objects.all().get(Term = Term, CategoryID = CategoryID_id).Mark
		mark = int(mark)
		if mark > 1:
			with connection.cursor() as cursor:
				cursor.execute(
				    "UPDATE index_vocabulary SET index_vocabulary.Mark = %s WHERE index_vocabulary.id = (SELECT index_vocabulary.id FROM index_vocabulary INNER JOIN index_category on index_vocabulary.CategoryID_id = index_category.id INNER JOIN index_user ON index_user.id = index_category.UserID_id WHERE index_user.id = '%s' AND index_vocabulary.Term = %s AND index_vocabulary.CategoryID_id = %s)" ,
				    [mark - 1, request.user.id, Term, CategoryID_id]
				)
			return render(request, 'learn.html') 
		else:
			return render(request, 'learn.html') 
	else:
		return render(request, 'login.html')

