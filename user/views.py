from django.shortcuts import render
from django.contrib.auth import authenticate
from index.models import User as User_english
from index.models import Category, Vocabulary
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
import re
from django.db import connection
def user(request):
	if request.user.is_authenticated:
		categoryContentExteition = {'categoryContentExteition': Category.objects.all().get(UserID = request.user.id, Name = "Google chrome extention"), 'categoryContent': Category.objects.filter(UserID = request.user.id, Is_Extention = False)}
		return render(request, 'indexUser.html',categoryContentExteition)
	else:
		return render(request, 'login.html')
def createCategoryInterface(request):
	if request.user.is_authenticated:
		 return render(request, 'createCategory.html')
	else:
		return render(request, 'login.html')
def addVocabulary(request):
	if request.user.is_authenticated:
		title = request.POST.get('title','')
		description = request.POST.get('description','')
		term = request.POST.getlist('term[]','')
		definition = request.POST.getlist('definition[]','')
		# Câu hỏi nếu trong quá trình tạo có 1 quá trình khác xen vào thì the last id có bị thay đổi theo hay không?
		Category.objects.create(UserID_id = request.user.id, Name = title,Description = description, Is_Extention = False)
		for x in range(len(term)):
			if term != "" or definition != "":
				Vocabulary.objects.create(CategoryID_id = Category.objects.latest('id').id, Term = term[x].strip(),Definition = definition[x].strip(), Mark = 0)
		return redirect('/login')
	else:
		return render(request, 'login.html')
def addVocabularyExtention(request, term, definition):
	if request.user.is_authenticated:
		extentionID = Category.objects.filter(Is_Extention = True, UserID_id = request.user.id)
		Vocabulary.objects.create(CategoryID_id = extentionID[0].id, Term = term.strip(),Definition = definition.strip(), Mark = 0)
		return redirect('/login')
	else:
		return render(request, 'login.html')
def deleteCategory(request, id):
	if request.user.is_authenticated:
		Category.objects.filter(UserID = request.user.id, id = id).delete()
		selectCategory = Category.objects.filter(UserID = request.user.id, Is_Extention = False)
		response = HttpResponse()
		for x in range(len(selectCategory)):
			response.writelines("<div class='col-12' id="+str(selectCategory[x].id)+"><div class='center'><p class="+"new_word"+"><a href="+"/chooseGame/"+ str(selectCategory[x].id) +">"+str(selectCategory[x].Name)+"</a></p><p class="+"mean"+">"+str(selectCategory[x].Description)+"</p><div class='function'></div><div class='function' style='float: right;'><i class='fa fa-edit' style='font-size:32px; margin-top: 11px;' onclick="+"showPopupEdit("+ str(selectCategory[x].id)+")""></i></div><div class='function' style='float: right;'><i class='fa fa-trash' style='font-size:32px; margin-top: 9px;' onclick="+"showPopup("+ str(selectCategory[x].id)+")""></i></div></div></div>")
		return response
	else:
		return render(request, 'login.html')
def updateCategory(request, id, name, description):
	if request.user.is_authenticated:
		Category.objects.filter(id = id, UserID_id = request.user.id).update(Name = name, Description = description)
		return render(request, 'indexUser.html')
	else:
		return render(request, 'login.html')
def chooseGame(request, id):
	if request.user.is_authenticated:
		newWord = {'newWord': Vocabulary.objects.filter(CategoryID_id=id), 'CategoryID':id}
		return render(request, 'Vocabulary.html', newWord)
	else:
		return render(request, 'login.html')
def tickNewWord(request,id):
	if request.user.is_authenticated:
		# Nếu chạy câu IF đầu tiên thì câu thứ 2 sẽ mặc định là đúng và câu lệnh IF thứ 2 sẽ tiếp tục chạy, do đó cần một biến trung gian để kiểm tra
		number = 0
		if Vocabulary.objects.get(id = id).Tick == False and number == 0:
			Vocabulary.objects.filter(id = id).update(Tick = 1)
			number = number + 1
		if Vocabulary.objects.get(id = id).Tick == True and number == 0:
			Vocabulary.objects.filter(id = id).update(Tick = 0)
			number = number + 1
		response = HttpResponse()
		response.writelines('<p>Tick success</p>')
		return response

	else:
		return render(request, 'login.html')
def updateVocabulary(request, id, Term, Definition):
	if request.user.is_authenticated:
		with connection.cursor() as cursor:
			cursor.execute(
			    "UPDATE index_vocabulary SET index_vocabulary.Term = %s, index_vocabulary.Definition =  %s WHERE index_vocabulary.id = (SELECT index_vocabulary.id FROM index_vocabulary INNER JOIN index_category on index_vocabulary.CategoryID_id = index_category.id INNER JOIN index_user ON index_user.id = index_category.UserID_id WHERE index_user.id = '%s' AND index_vocabulary.id = '%s')" ,
			    [Term, Definition, request.user.id,id]
			)
		return render(request, 'indexUser.html')
	else:
		return render(request, 'login.html')
def deleteVocabulary(request, id):
	if request.user.is_authenticated:
		with connection.cursor() as cursor:
			cursor.execute(
			    "DELETE FROM index_vocabulary WHERE index_vocabulary.id = (SELECT index_vocabulary.id FROM index_vocabulary INNER JOIN index_category on index_vocabulary.CategoryID_id = index_category.id INNER JOIN index_user ON index_user.id = index_category.UserID_id WHERE index_user.id = '%s' AND index_vocabulary.id = '%s')" ,
			    [request.user.id,id]
			)
		return render(request, 'indexUser.html')
	else:
		return render(request, 'login.html')