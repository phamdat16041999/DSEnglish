from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
import re
from .models import Category
from django.shortcuts import redirect
# Create your views here.
def index(request):
   return render(request, 'index.html')
def login(request):
	if request.user.is_authenticated:
		categoryContentExteition = {'categoryContentExteition': Category.objects.all().get(UserID = request.user.id, Name = "Google chrome extention"), 'categoryContent': Category.objects.filter(UserID = request.user.id, Is_Extention = False)}
		return render(request, 'user/Index.html',categoryContentExteition)
	else:
		return render(request, 'login.html')
def userIndex(request):
	if request.method == 'POST':
	    username = request.POST.get('username','')
	    password = request.POST.get('password','')
	    user = authenticate(username=username, password=password)
	    # return render(request, 'login.html')
	    if(user is not None):
	        if user.is_active:
	            request.session.set_expiry(86400)
	            auth_login(request, user)
	            # Tao co so du lieu cho nguoi dung Chrome extention
	            if len(Category.objects.filter(UserID = user.id, Is_Extention = True)) == 0:
	            	Category.objects.create(UserID_id = int(user.id), Name = "Google chrome extention",Description = "Vocabulary added from the Google Chrome extension", Is_Extention = True)
	            	categoryContentExteition = {'categoryContentExteition': Category.objects.all().get(UserID = request.user.id, Name = "Google chrome extention"), 'categoryContent': Category.objects.filter(UserID = request.user.id, Is_Extention = False)}
	            	return redirect('/login')
	            if len(Category.objects.filter(UserID = user.id, Is_Extention = True)) == 1:
	            	# print(Category.objects.all().get(Name = "Google chrome extention").Is_Extention)
	            	categoryContentExteition = {'categoryContentExteition': Category.objects.all().get(UserID = request.user.id, Name = "Google chrome extention"), 'categoryContent': Category.objects.filter(UserID = request.user.id, Is_Extention = False)}
	            	return redirect('/login')
	if request.user.is_authenticated:
		categoryContentExteition = {'categoryContentExteition': Category.objects.all().get(UserID = request.user.id, Name = "Google chrome extention"), 'categoryContent': Category.objects.filter(UserID = request.user.id, Is_Extention = False)}
		return redirect('/login')
	if request.user.is_authenticated == False:
	   	return redirect('/login')
def createAccount(request):
   return render(request, 'create account.html')
def insertAccount(request):
	firstName = request.POST.getlist('firstName')
	lastName = request.POST.getlist('lastName')
	userName = request.POST.getlist('userName')
	email = request.POST.getlist('email')
	password = request.POST.getlist('password')
	validate = 0
	int(validate)
	if(len(userName[0]) < 6 or len(password[0]) < 6):
		validate = validate + 1
	if(re.match("^[a-zA-Z0-9_]*$", userName[0]) == None or re.match("^[a-zA-Z0-9_]*$", password[0]) == None):
		validate = validate + 1
	if(validate > 0):
		return render(request, 'errorAccount.html')
	# Kiểm tra xem tài khoản tồn tại hay chưa
	if(validate == 0):
		if len(User.objects.filter(username = userName[0])) == 0:
			User.objects.create_user(first_name = firstName[0], last_name = lastName[0],username = userName[0], email=email[0], password= password[0])
			return render(request, 'index.html')
		if len(User.objects.filter(username = userName[0])) == 1:
			error = {'error': 'Username already exists, please try a different username'}
			return render(request, 'create account.html', error)
def learn(request):
	if request.user.is_authenticated:
		# print(request.user.id)
		return render(request, 'user/learn.html')
	else:
		return render(request, 'login.html')

def logout(request):
	django_logout(request)
	return render(request, 'index.html')
# Kiểm tra xem tài khoản tồn tại hay chưa
def checkDuplicateAccount(request):
	userName = request.GET.getlist('userName')
	if len(User.objects.filter(username = userName[0])) == 0:
		response = HttpResponse()
		response.writelines('<p></p>')
		return response
	if len(User.objects.filter(username = userName[0])) == 1:
		response = HttpResponse()
		response.writelines('<p>Account already exists</p>')
		return response
