
from django.shortcuts import render,redirect

from blog.models import Blog, Category
from project1.forms import RegistrationForm
from social.models import About
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def home(request):
    featured_posts=Blog.objects.filter(is_featured=True,status='Published')
    posts=Blog.objects.filter(is_featured=False,status='Published')
    try:
        about=About.objects.get()
    except:
        about=None
    context={
        'featured_posts':featured_posts,
        'posts':posts,
        'about':about
    }
    return render(request,'home.html',context)

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(home)
        else:
            print(form.errors)
    else:
        form=RegistrationForm()
    context={
        'form':form,
    }
    return render(request,'register.html',context)

def login(request):
    if request.method=='POST':
        uform=AuthenticationForm(request,request.POST)
        if uform.is_valid():
            username=uform.cleaned_data['username']
            password=uform.cleaned_data['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
            return redirect('home')
    uform=AuthenticationForm()
    context={
        'uform':uform,
    }
    return render(request,'login.html',context)

def logout(request):
    auth.logout(request)
    return redirect('login')