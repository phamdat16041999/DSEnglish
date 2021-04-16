from django.shortcuts import render
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
from index.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
# Send email	
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

def createAccount(request):
	return render(request, 'create account.html')
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
def insertAccount(request):
    firstName = request.POST.getlist('firstName')
    lastName = request.POST.getlist('lastName')
    userName = request.POST.getlist('userName')
    email = request.POST.getlist('email')
    password = request.POST.getlist('password')
    random_code = random_password(12)
    if len(User.objects.filter(username = userName[0])) == 0:
        User.objects.create_user(first_name = firstName[0], last_name = lastName[0],username = userName[0], email=email[0], password= password[0], is_active = False, code = random_code)
        # send email
        CLIENT_SECRET_FILE = 'C:/Users/phamdat/dsenglish/createAccount/client_secret.json'
        API_NAME = "gmail"
        API_VERSION = "v1"
        SCOPES = ["https://mail.google.com/"]
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        emailMsg = "Your verification code is: " + random_code
        mimeMessage = MIMEMultipart()
        mimeMessage["to"] = email[0]      #datptgch17575@fpt.edu.vn
        mimeMessage["subject"] = "Authentic"
        mimeMessage.attach(MIMEText(emailMsg, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        message = service.users().messages().send(userId="me", body={"raw": raw_string}).execute()
        print(User.objects.latest('id').id);
        userId = {'userId': User.objects.latest('id').id}
        return render(request, 'authenticEmail.html', userId)
    if len(User.objects.filter(username = userName[0])) == 1:
        error = {'error': 'Username already exists, please try a different username'}
        return render(request, 'create account.html', error)

def authenticEmail(request, id):
    code = request.POST.getlist('code')
    correctCode = User.objects.get(id = id).code
    if(code[0] == correctCode):
        User.objects.filter(id = id).update(is_active = True)
        return redirect("/")
    else:
        error = {'error': 'Your verification code is incorrect', 'userId': id}
        return render(request, 'authenticEmail.html', error)