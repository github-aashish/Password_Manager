from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import random

# Create your views here.
def login(request):
    message = None
    if 'logid' in request.session:
        return redirect(home)
    else:
        if request.method == 'POST':
            Email = request.POST.get('email')
            Password = request.POST.get('password')
            try:
                client = User.objects.get(email=Email, password=Password)
            except:
                client = None
            if client is not None:
                request.session['logid']=client.id
                request.session['logname']=client.name
                request.session.save()
                return redirect(home)
            else:
                message = "Invalid Email or Passsword"
                return render(request, 'login.html',locals())
        else:
            return render(request, 'login.html')
def signup(request):
    message = None
    if request.method == 'POST':
        Name =  request.POST.get('uname')
        Mobile = request.POST.get('mobile')
        Email = request.POST.get('email')
        Password = request.POST.get('password')
        try:
            client_exist = User.objects.get(email=Email)
        except:
            client_exist = None
            
        if client_exist is None:
            client = User(name=Name, mobile=Mobile, email=Email, password=Password)
            client.save()
            return redirect(login)
        else:
            message = "User with same Email Already Exist!"
            return render(request, 'signup.html',locals())
            
    else:
        return render(request, 'signup.html',locals())
    
def logout(request):
    request.session.clear()
    return redirect(login)

def home(request):
    uid = request.session['logid']
    try:
        client = User.objects.get(id=uid)
        client_passwords = Passwords.objects.filter(user=client).values()
    except:
        client_passwords = None
    return render(request, 'index.html',locals())
    
def add_pass(request):
    if request.method == 'POST':
        uid = request.session['logid']
        website = request.POST.get('webname')
        password = request.POST.get('password')
        try:
            client = User.objects.get(id=uid)
        except:
            client = None
        if  client is not None:
            shift = random.randint(4, 9)
            encryption = encrypt(str(password),shift)
            print("original",password)
            print("Encrypted",encryption)
            Generated_Pass = Passwords(user=client,site=website,password=encryption,shifts=shift)
            Generated_Pass.save()
            return redirect(home)
        else:
            return redirect(login)
    else:
        return render(request, 'addpass.html')
    
def check_password(request,web_id):
    message = None
    website_id = web_id
    uid = request.session['logid']
    if request.method == 'POST':
        master_password = request.POST.get('password')
        try:
            client_exist = User.objects.get(id=uid,password=master_password)
        except:
            client_exist = None
        if client_exist is not None:
            web_password = Passwords.objects.get(id=website_id)
            enc_password = web_password.password
            shift = web_password.shifts
            password = decrypt(enc_password, shift)
            return render(request,'View.html',locals())
        else:
            message = "Incorrect Master Password"
            return render(request, 'master.html', locals())
        
    else:
        return render(request,'master.html',locals())
        
def encrypt(text, shift):
    result = ""
    
    # Traverse through the text
    for char in text:
        # Encrypt uppercase letters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        # Encrypt lowercase letters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        elif char.isdigit():
            result += chr((ord(char) + shift - 48) % 10 + 48)
        # For non-alphabetic characters, add them as they are
        else:
            result += char
            
    return result

def decrypt(text, shift):
    result = ""
    
    # Traverse through the text
    for char in text:
        # Decrypt uppercase letters
        if char.isupper():
            result += chr((ord(char) - shift - 65) % 26 + 65)
        # Decrypt lowercase letters
        elif char.islower():
            result += chr((ord(char) - shift - 97) % 26 + 97)
        elif char.isdigit():
            result += chr((ord(char) - shift - 48) % 10 + 48)
        # For non-alphabetic characters, add them as they are
        else:
            result += char
            
    return result
