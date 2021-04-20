from django.shortcuts import render
from django.contrib.auth import authenticate
from index.models import User as User_english
from index.models import Category, Vocabulary
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User

def login(request):
	if request.user.is_authenticated:
		categoryContentExteition = {'categoryContentExteition': Category.objects.all().get(UserID = request.user.id, Name = "Google chrome extention"), 'categoryContent': Category.objects.filter(UserID = request.user.id, Is_Extention = False)}
		return render(request, 'indexUser.html',categoryContentExteition)
	else:
		return render(request, 'login.html')
def loginFunction(request):
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
	    else:
	    	return render(request, 'login.html', {"error":"The account and password are incorrect"})
	if request.user.is_authenticated:
		categoryContentExteition = {'categoryContentExteition': Category.objects.all().get(UserID = request.user.id, Name = "Google chrome extention"), 'categoryContent': Category.objects.filter(UserID = request.user.id, Is_Extention = False)}
		return redirect('/login')
	if request.user.is_authenticated == False:
	   	return redirect('/login')
def logout(request):
	django_logout(request)
	return render(request, 'index.html')