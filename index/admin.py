from django.contrib import admin
from .models import Category, Vocabulary
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'UserID', 'Name', 'Description']
    list_filter = ['Name']
    search_fields = ['Name']
admin.site.register(Category, CategoryAdmin)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ['Term', 'Definition', 'CategoryID']
    list_filter = ['CategoryID']
    search_fields = ['CategoryID']
admin.site.register(Vocabulary, VocabularyAdmin)