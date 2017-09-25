# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
from datetime import datetime
from .forms import *
import bcrypt
def index(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            request.session["id"] = User.objects.get(email=form.cleaned_data["email"]).id
            return redirect("/dashboard")
    else:
        form = SignInForm()
    return render(request, "user_dashboard/index.html", {'form': form})
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            if not User.objects.all():
                newuser = User.objects.create(first_name=form["first_name"], last_name=form["last_name"], email=form["email"], hashed_pw=bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt()), admin=9)
                request.session["id"] = newuser.id
                return redirect("/dashboard")
            else:
                newuser = User.objects.create(first_name=form["first_name"], last_name=form["last_name"], email=form["email"], hashed_pw=bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt()))
                request.session["id"] = newuser.id
                return redirect("/dashboard")
    else:
        form = RegisterForm()
    return render(request, "user_dashboard/register.html", {'form': form})
def dashboard(request):
    if "id" not in request.session:
        return redirect("/signin")
    context = {
        "user" : User.objects.get(id=request.session["id"]),
        "all_users" : User.objects.all()
    }
    return render(request, "user_dashboard/dashboard.html", context)
def logout(request):
    request.session.clear()
    return redirect("/signin")
def create(request):
    if User.objects.get(id=request.session["id"]).admin != 9:
        return redirect("/dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            newuser = User.objects.create(first_name=form["first_name"], last_name=form["last_name"], email=form["email"], hashed_pw=bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt()))
            return redirect("/dashboard")
    else:
        form = RegisterForm()
    return render(request, "user_dashboard/add.html", {'form': form})
def profile(request):
    user = User.objects.filter(id=request.session["id"])
    data = {
            "first_name" : user[0].first_name,
            "last_name" : user[0].last_name,
            "email" : user[0].email,
        }
    infoform = UpdateInfo(data)
    passform = ChangePassword()
    if user[0].description:
        descform = EditDescription({"description" : user[0].description})
    else:
        descform = EditDescription()
    if request.method == "POST":
        if "email" in request.POST:
            infoform = UpdateInfo(request.POST)
            if infoform.is_valid():
                form = infoform.cleaned_data
                user.update(first_name=form["first_name"], last_name=form["last_name"], email=form["email"])
                return redirect("/dashboard")
        elif "password" in request.POST:
            passform = ChangePassword(request.POST)
            if passform.is_valid():
                form = passform.cleaned_data
                user.update(hashed_pw=bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt()))
                return redirect("/dashboard")
        elif "description" in request.POST:
            descform = EditDescription(request.POST)
            if descform.is_valid():
                form = descform.cleaned_data
                user.update(description=form["description"])
                return redirect("/dashboard")
    context = {
        "infoform" : infoform,
        "passform" : passform,
        "descform" : descform
    }
    return render(request, "user_dashboard/editprofile.html", context)
def edit(request, id):
    if User.objects.get(id=request.session["id"]).admin != 9:
        return redirect("/dashboard")
    user = User.objects.filter(id=int(id))
    data = {
            "first_name" : user[0].first_name,
            "last_name" : user[0].last_name,
            "email" : user[0].email,
            "user_level" : user[0].admin
        }
    infoform = UpdateInfoAdmin(data)
    passform = ChangePassword()
    if request.method == "POST":
        if "email" in request.POST:
            infoform = UpdateInfoAdmin(request.POST)
            if infoform.is_valid():
                form = infoform.cleaned_data
                user.update(first_name=form["first_name"], last_name=form["last_name"], email=form["email"], admin=form["user_level"])
                return redirect("/dashboard")
        elif "password" in request.POST:
            passform = ChangePassword(request.POST)
            if passform.is_valid():
                form = passform.cleaned_data
                user.update(hashed_pw=bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt()))
                return redirect("/dashboard")
    context = {
        "user" : user[0],
        "infoform" : infoform,
        "passform" : passform,
    }
    return render(request, "user_dashboard/edituser.html", context)
def show(request, id):
    if "id" not in request.session:
        return redirect("/signin")
    context = {
        "messform" : MessageForm(),
        "commform" : CommentForm(),
        "user" : User.objects.get(id=int(id)),
        "messages" : Message.objects.filter(recipient__id=int(id)).order_by("-created_at"),
        "comments" : Comment.objects.all(),
    }
    return render(request, "user_dashboard/wall.html", context)
def addmessage(request, id):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            Message.objects.create(message=form["message"], messager=User.objects.get(id=request.session["id"]), recipient=User.objects.get(id=int(id)))
    return redirect("/users/show/"+id)
def addcomment(request, user_id, mess_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            Comment.objects.create(comment=form["comment"], commenter=User.objects.get(id=request.session["id"]), message=Message.objects.get(id=int(mess_id)))
            return redirect("/users/show/"+user_id)
    return redirect("/users/show/"+user_id)