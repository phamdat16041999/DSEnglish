from django.shortcuts import render
from django.contrib.auth import authenticate
from index.models import User as User_english
from index.models import Category, Vocabulary
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User

import string
import random
import pickle
import re
import os
import base64
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import HttpResponse
from django.shortcuts import redirect

def random_password(length):
    LETTERS = string.ascii_letters
    DIGITS = string.digits
    
    x = list(f'{LETTERS}{DIGITS}')
    random.shuffle(x)
    code = random.choices(x, k = length)
    code = ''.join(code)
    return(code)
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep="-")
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f"token_{API_SERVICE_NAME}_{API_VERSION}.pickle"
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, "wb") as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, "service created successfully")
        return service
    except Exception as e:
        print("Unable to connect!")
        print(e)
        return None
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
def forgotPassword(request):
	return render(request, 'forgotPassword.html')
def checkEmail(request):
	email = request.POST.get('email','')
	checkEmail = User_english.objects.filter(email = email)
	if(len(checkEmail) > 0):
		random_code = random_password(12)
		CLIENT_SECRET_FILE = './client_secret.json'
		API_NAME = "gmail"
		API_VERSION = "v1"
		SCOPES = ["https://mail.google.com/"]
		service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
		emailMsg = "Please click on this link to change your password:" + "http://localhost:8000/login/changePasswordInterface/" + str(checkEmail[0].id) + "/" + random_code
		mimeMessage = MIMEMultipart()
		mimeMessage["to"] = email
		mimeMessage["subject"] = "Change password"
		mimeMessage.attach(MIMEText(emailMsg, 'plain'))
		raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
		message = service.users().messages().send(userId="me", body={"raw": raw_string}).execute()
		updateCode = User_english.objects.get(id = checkEmail[0].id)
		updateCode.code = random_code
		updateCode.save()
		return render(request, 'forgotPassword.html', {"error":"Please check your email for password change"})
	else:
		return render(request, 'forgotPassword.html', {"error":"Email does not exist"})
def changePasswordInterface(request, id, code):
	user = User_english.objects.filter(id = id, code = code)
	if(len(user) == 0):
		return render(request, 'notFound404.html')
	else:
		return render(request, 'changePassword.html', {"id":id})
def changePassword(request):
	if request.method == 'POST':
		password = request.POST.get('password','')
		UserID = request.POST.get('UserID','')
		random_code = random_password(12)
		user = User_english.objects.get(id = UserID)
		user.set_password(password)
		user.code = random_code
		user.save()
		return redirect('/')
	else:
		return render(request, 'notFound404.html')