from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json
from datetime import datetime
import random
import os
import docx

# main page function

def index(request):
    # if not request.user.is_authenticated:
    #     return redirect("login")
    return render(request, 'index.html')

def documents(request):
    return render(request, 'privacy.html')

# def select_random_native_speaker():
#     all_speakers = list(native_speaker.objects.all())
#     if len(all_speakers) > 0:
#         return random.choice(all_speakers)
#     else:
#         return None
def para2text(p):
    rs = p._element.xpath('.//w:t')
    return u" ".join([r.text for r in rs])

def getWordText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        #fullText.append(para.text)
        ans = para2text(para)
        fullText.append(ans)
        #print(ans)
    return '.'.join(fullText)

def getTxtText(filename):
    myfile = open(filename, "r")
    return myfile.read()


def count_words(filename):
    count = 0

    fileType = filename.split(".")[-1]

    if fileType == "docx":
        mywordfile = getWordText(filename)
    
    elif fileType == "txt":
        mywordfile = getTxtText(filename)
    
    elif fileType == "pdf":
        return 0

    else:
        mywordfile = filename
        fileType = "Plain text"

    mywordfile = mywordfile.replace(",", " ")
    mywordfile = mywordfile.replace(".", " ")
    mywordfile = mywordfile.replace("  ", " ")
    mywordfile = mywordfile.replace("\n", " ")
    mywordfile = mywordfile.replace("\r", " ")
    mywordfile = mywordfile.replace("\t", " ")

    new_str = mywordfile.split(" ")

    print(new_str)

    for i in new_str:
        if len(i) > 0:
            count += 1

    fileType = fileType.upper()

    return (count, fileType)

def submitwork(request):
    if request.method == 'POST':
        category = request.POST['category']
        custommsg = request.POST['custommsg']
        textwritten = None
        targetfile = None
        if 'textwritten' in request.POST:
            if len(request.POST['textwritten']) > 0:
                textwritten = request.POST['textwritten']

        if 'targetfile' in request.FILES:
            targetfile = request.FILES['targetfile']

        print(category)
        print(custommsg)
        print(textwritten)
        print(targetfile)


        new_order = order(
            placed_by = request.user,
            text_type = category,
            plane_text = textwritten,
            attachment = targetfile,
            special_note = custommsg
        )

        new_order.save()

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if targetfile:
            if str(targetfile).split(".")[1] != "pdf":

                file_path = os.path.join(BASE_DIR, "media\work\{}".format(str(targetfile)))
                answer = count_words(file_path)
                new_order.total_words = answer[0]
                new_order.file_type = answer[1]
                new_order.save()
            else:
                new_order.file_type = "PDF"
                new_order.save()
        else:
            answer = count_words(textwritten)
            new_order.total_words = answer[0]
            new_order.file_type = answer[1]
            if new_order.total_words < 200:
                new_order.is_confirmed = False
            new_order.save()

             

        # print(count_words(targetfile))

        messages.info(request, "Your text has been submitted for proofread")

        return redirect("profile")
        
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

def upload_work(request):
    if not request.user.is_authenticated:
        return redirect("index")

    return render(request, 'upload-work.html')

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


    if order.objects.filter(placed_by = request.user).exists():
        context['orders'] = order.objects.filter(placed_by = request.user).order_by("-id")

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
        birth = request.POST['birth']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
            "birth":birth
        }

        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name, email=birth)
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

