from django.urls import path
from . import views
from . import userView, learnView
urlpatterns = [
   path('', views.index),
   path('login', views.login),
   path('createAccount', views.createAccount),
   # path('insertAccount/<str:firstName>/<str:lastName>/<str:userName>/<str:email>/<str:password>', views.insertAccount),
   path('insertAccount', views.insertAccount),
   path('userIndex', views.userIndex),
   path('logout', views.logout),
   path('checkDuplicateAccount', views.checkDuplicateAccount),
   # userView
   path('addVocabularyByExtention', userView.addVocabularyByExtention),
   path('createCategoryInterface', userView.createCategoryInterface),
   path('addVocabulary', userView.addVocabulary),
   path('chooseGame/<int:id>/', userView.chooseGame),
   path('deleteCategory/<int:id>/', userView.deleteCategory),
   path('deleteVocabulary/<int:id>/', userView.deleteVocabulary),
   path('tickNewWord/<int:id>/', userView.tickNewWord),
   path('updateCategory/<int:id>/<str:name>/<str:description>/', userView.updateCategory),
   path('updateVocabulary/<int:id>/<str:Term>/<str:Definition>/', userView.updateVocabulary),
   # learnView
   path('learn/<int:id>/', learnView.learn),
   path('write/<int:id>/', learnView.write),
   path('flipCard/<int:id>/', learnView.flipCard),
   path('memoryCard/<int:id>/', learnView.memoryCard),
   path('plusPoints/<str:Term>/<str:CategoryID_id>/', learnView.plusPoints),
   path('subtractPoints/<str:Term>/<str:CategoryID_id>/', learnView.subtractPoints),
]