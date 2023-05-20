from django.shortcuts import render, HttpResponseRedirect,redirect
from  .forms import signupform,loginform,postform
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import post

from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import Group



# Create your views here.
#home
def home(request):
    posts = post.objects.all()
    print(posts)
    return render(request, 'blog/home.html', {'posts': posts})

#about
def about(request):
    return render(request, 'blog/about.html')

#contact
def contact(request):
    return render(request, 'blog/contact.html')

#dashboard
def dashboard(request):
    if request.user.is_authenticated:
     posts = post.objects.all()
     user = request.user
     full_name = user.get_full_name()
     gps = user.groups.all()
     return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name':full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

#logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#signup
def user_signup(request):
 if request.method == "POST":
    form = signupform(request.POST)
    if form.is_valid():
        messages.success(request, "Congratulations!! You have become an Author. ")
        user= form.save()
        group = Group.objects.get(name='Author')
        user.groups.add(group)
 else:
  form = signupform()
 return render(request, 'blog/signup.html', {'form':form})

#login
def user_login(request):
 if not request.user.is_authenticated:
      if request.method == "POST":
            form = loginform( data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'logged in successfully !!')
                    #return HttpResponseRedirect('/dashboard/')
                    return redirect('/dashboard/')
      else:
            form = loginform()
      return render(request, 'blog/login.html', {'form': form})
 else:
    return HttpResponseRedirect('/dashboard/')

# Add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = postform(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = post(title=title, desc=desc)
                pst.save()
                form = postform()
        else:
            form = postform()
        return render(request, 'blog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')


# update post/edit post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = post.objects.get(pk=id)
            form = postform(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
         pi = post.objects.get(pk=id)
         form = postform(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


# delete post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')