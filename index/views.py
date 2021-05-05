from django.shortcuts import render
from django.http import HttpResponse
from index.models import Contacts
def index(request):
	return render(request, 'index.html')
def Overview(request):
	return render(request, 'Overview.html')
def notFound404(request):
	return render(request, 'notFound404.html')
def contacts(request, firstName, lastName, email, messenger):
	Contacts.objects.create(FirstName = firstName, LastName = lastName, Email = email, Messenger = messenger)
	response = HttpResponse()
	response.writelines('Success')
	return response