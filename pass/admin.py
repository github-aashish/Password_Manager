from django.contrib import admin
from .models import *

# Register your models here.
class showUsers(admin.ModelAdmin):
    list_display = ['name','email']
    
class showPasswords(admin.ModelAdmin):
    list_display = ['user','site']
    
    
    
    
admin.site.register(User,showUsers)
admin.site.register(Passwords,showPasswords)
