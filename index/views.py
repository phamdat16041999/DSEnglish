from django.shortcuts import render
def index(request):
	return render(request, 'index.html')
def Overview(request):
	return render(request, 'Overview.html')
def notFound404(request):
	return render(request, 'notFound404.html')