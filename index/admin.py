from django.contrib import admin

from .models import User, Contacts
# Register your models here.
admin.site.register(User)
class ContactsAdmin(admin.ModelAdmin):
	list_display = ['Email', 'LastName', 'Messenger']
	list_filter = ['Read']
	search_fields = ['Read']
admin.site.register(Contacts, ContactsAdmin)