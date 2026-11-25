from django.shortcuts import render,redirect
from .models import *
import qrcode
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate ,login, logout
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import logging
logger=logging.getLogger('django')
# Create your views here.
def index(request):
    momo=None
    category=None
    try:
        category=Category.objects.all()
        catid = request.GET.get("category")
        if catid == 'all':
            momo=Momo.objects.all()
        elif catid:
            momo = Momo.objects.filter(category=catid)
        else:
            momo=Momo.objects.all()

        if request.method =='POST':
            name=request.POST['name']
            phone=request.POST['number']
            email=request.POST['email']
            message=request.POST['message']
            Contact.objects.create(name=name,phone=phone,email=email,message=message)
            return redirect('index')
    except Exception as e:
        logger.error(e,exc_info=True)
    context={
        'category':category ,
        'momo':momo,
        }
    return render(request,'core/index.html',context)

@login_required(login_url='log_in')
def about(request):
    return render(request,'core/about.html')
def contact(request):
    return render(request,'core/contact.html')


@login_required(login_url='log_in')
def menu(request):
    qr=qrcode.make('http://127.0.0.1:8000/menu/')
    qr.save("menu.png")
    
    category=Category.objects.all()
    return render(request,'core/menu.html',{'category':category})
def services(request):
    return render(request,'core/services.html')
def testemonial(request):
    return render(request,'core/testemonial.html')
def privacy(request):
    return render(request,'core/privacy.html')
def terms(request):
    return render(request,'core/terms.html')
def help(request):
    return render(request,'core/help.html')

# Authentication part start

def register(request):
    if request.method == "POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']

        if password == password1:
            error=[]
            if User.objects.filter(username=username).exists():
                error.append('Username already exists')
        
            if User.objects.filter(email=email).exists():
                error.append('Email already used')
            if not re.search(r'[A-Z]',password):
                error.append('Your password must contain atleast an upper case')
            if not re.search(r'\d',password):
                error.append('Your password must contain atleast one digit')
            if not re.search(r'\W',password):
                error.append('Your password must contain atleast special character')
                
            try:
                validate_password(password)
                if not error:

                   User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                   messages.success(request,"Registred successfully")
                   return redirect('register')
                else:
                    for i in error:
                        messages.error(request,i)
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')

        else:
            messages.error(request,'Password doesnot match')
            redirect('register')

    
    return render(request,'auth/register.html')
def log_in(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        remember_me=request.POST.get('remember_me')
    
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Username not registered yet!!')
            return redirect('log_in')


        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)

            if remember_me:
                print("session")
                request.session.set_expiry(12222)
                
            else:
                request.session.set_expiry(0)


            next=request.POST.get('next','')
            return redirect(next if next else 'index')
        else:
            messages.error(request,'Password doesnot match with username')
            return redirect('log_in')
    next=request.GET.get('next','')
    return render(request,'auth/login.html',{'next':next})
def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == 'POST':

        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
        
    return render(request,'auth/change_password.html',{'form':form})
 
