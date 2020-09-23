from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json
from datetime import datetime

# main page function

def index(request):
    # if not request.user.is_authenticated:
    #     return redirect("login")
    return render(request, 'index.html')

def documents(request):
    return render(request, 'privacy.html')

def becomenative(request):
    if request.method == 'POST':
        myFile = request.FILES['doc']

        org_1 = request.POST['org_1']
        year_1 = request.POST['year_1']
        type_1 = request.POST['type_1']

        org_2 = request.POST['org_2']
        year_2 = request.POST['year_2']
        type_2 = request.POST['type_2']

        org_3 = request.POST['org_3']
        year_3 = request.POST['year_3']
        type_3 = request.POST['type_3']

        org_4 = request.POST['org_4']
        year_4 = request.POST['year_4']
        type_4 = request.POST['type_4']

        print('org_1', org_1)
        print('year_1', year_1)
        print('type_1', type_1)
        print()
        print('org_2', org_2)
        print('year_2', year_2)
        print('type_2', type_2)
        print()
        print('org_3', org_3)
        print('year_3', year_3)
        print('type_3', type_3)
        print()
        print('org_4', org_4)
        print('year_4', year_4)
        print('type_4', type_4)

        new_native = native_speaker(
            which_user = request.user,
            g_passport = myFile,
            org_1 = org_1,
            year_1 = year_1,
            type_1 = type_1,
            org_2 = org_2,
            year_2 = year_2,
            type_2 = type_2,
            org_3 = org_3,
            year_3 = year_3,
            type_3 = type_3,
            org_4 = org_4,
            year_4 = year_4,
            type_4 = type_4,
        )

        new_native.save()


    return redirect("profile")



# main page
def profile(request):
    if not request.user.is_authenticated:
        return redirect("index")

    context = {
        'date_joined': request.user.date_joined.date(),
    }

    if native_speaker.objects.filter(which_user = request.user).exists():
        if native_speaker.objects.get(which_user = request.user).isAccepted:
            context['status'] = "You are now a native speaker"
        else:
            context['status'] = "Native speaker request has been sent"




    # print(date_joined)

    return render(request, 'profile-page.html', context)


# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")

