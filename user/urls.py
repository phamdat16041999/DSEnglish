from django.contrib import admin
from django.urls import path
from .import views, learnView

urlpatterns = [
    path('', views.user),
    path('/createCategoryInterface', views.createCategoryInterface),
    path('/addVocabulary', views.addVocabulary),
    path('/deleteCategory/<int:id>/', views.deleteCategory),
    path('/updateCategory/<int:id>/<str:name>/<str:description>/', views.updateCategory),
    path('/chooseGame/<int:id>/', views.chooseGame),
    path('/tickNewWord/<int:id>/', views.tickNewWord),
    path('/updateVocabulary/<int:id>/<str:Term>/<str:Definition>/', views.updateVocabulary),
    path('/deleteVocabulary/<int:id>/', views.deleteVocabulary),
    # learnView
	path('/learn/<int:id>/', learnView.learn),
	path('/write/<int:id>/', learnView.write),
    path('/speak/<int:id>/', learnView.speak),
	path('/flipCard/<int:id>/', learnView.flipCard),
	path('/memoryCard/<int:id>/', learnView.memoryCard),
	path('/plusPoints/<str:Term>/<str:CategoryID_id>/', learnView.plusPoints),
	path('/subtractPoints/<str:Term>/<str:CategoryID_id>/', learnView.subtractPoints),
    path('/addVocabularyExtention/<str:term>/<str:definition>/', views.addVocabularyExtention),
]