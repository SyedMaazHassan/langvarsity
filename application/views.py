from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse
import json
from datetime import datetime
import random
import os
import docx
import hashlib as hl
import six, base64

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

# to deliver the work
def deliverNow(request):
    if request.method == 'POST':
        orderID = request.POST['orderID']
        deliveryFile = request.FILES['targetfile']

        print("orderID =>", orderID)
        print("deliveryFile =>", deliveryFile)

        new_delivery = deliveries(
            revised_file = deliveryFile,
            order = order.objects.get(id = int(orderID))
        )

        new_delivery.save()

        return redirect("profile")

# complete or ask for revisio
def make_it_as(request):
    output = {}
    if request.method == "GET":
        if request.is_ajax():
            task = int(request.GET['task'])
            orderID = int(request.GET['orderID'])

            print("task =>", task)
            print("orderID =>", orderID)

            if order.objects.filter(id = orderID).exists():
                particular_order = order.objects.get(id = orderID)

                if task == 1:
                    particular_order.order_status = "COMPLETED"
                else:
                    particular_order.order_status = "IN-REVISION"

                particular_order.save()

                output['status'] = 1

            # +1 for accept
            # -1 for revision

    return JsonResponse(output)


def inbox(request, person_id):
    if not request.user.is_authenticated:
        return redirect("index")

    print(person_id)
    context = {}

    if User.objects.filter(id = person_id).exists():
        second_person = User.objects.get(id = person_id)

        user1_isNative = native_speaker.objects.filter(which_user = request.user).exists()
        user2_isNative = native_speaker.objects.filter(which_user = second_person).exists()

        native = ""
        non_native = ""

        if user1_isNative:
            native = native_speaker.objects.get(which_user = request.user)
            non_native = second_person
        elif user2_isNative:
            native = native_speaker.objects.get(which_user = second_person)
            non_native = request.user
        else:
            return redirect("index")

        print(native.which_user.username)
        print(non_native.username)

        condition = order.objects.filter(placed_by = non_native, alloted_to = native).exists()

        if condition:
            context['second_person'] = second_person

            cursor = connection.cursor()
            cursor.execute('''
            
                SELECT * FROM application_allmsg
                WHERE
                    (sender_id = {} AND receiver_id = {})
                OR
                    (sender_id = {} AND receiver_id = {})
                ORDER BY 
                    id;
            
            '''.format(native.which_user.id, non_native.id, non_native.id, native.which_user.id))

            all_msgs = cursor.fetchall()

            for i in range(len(all_msgs)):
                all_msgs[i] = list(all_msgs[i])
                sender = User.objects.get(id = all_msgs[i][4])
                receiver = User.objects.get(id = all_msgs[i][3])
                all_msgs[i][1] = decode(generate_code(sender, receiver), all_msgs[i][1])

            context['all_msgs'] = all_msgs
            return render(request, "inbox.html", context)

    return redirect("index")


def generate_code(sender, receiver):
    strs = sender.username + receiver.username
    code_hash = hl.md5(strs.encode())
    return code_hash.hexdigest()

def decode(key, string):
    string = string[2:-1]
    string = base64.urlsafe_b64decode(bytes(string.encode()) + bytes("===".encode()))
    string = string.decode('latin') if six.PY3 else string
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string

def sendMsg(request):
    output = {}
    if request.method == "GET" and request.is_ajax():
        to = int(request.GET['to'])
        try:
            to = User.objects.get(id = to)
        except:
            output['status'] = False
            return JsonResponse(output)

        msg = request.GET['msg']

        print("to =>", to.first_name)
        print("msg =>", msg)

        new_msg = allMsg(
            sender = request.user,
            receiver = to,
            message = msg
        )

        new_msg.save()

        output['status'] = True

        return JsonResponse(output)

def getMsgs(request):
    output = {}
    if request.user.is_authenticated:
        if request.method == "GET" and request.is_ajax():
            msg_present = int(request.GET['msg_present'])
            to = int(request.GET['to'])
            try:
                receiver = User.objects.get(id = to)
                sender = request.user

                # everyting is fine, write your valid code here.
                cursor = connection.cursor()
                cursor.execute('''
                
                    SELECT * FROM application_allmsg
                    WHERE
                        (sender_id = {} AND receiver_id = {})
                    OR
                        (sender_id = {} AND receiver_id = {})
                    ORDER BY 
                        id;
                
                '''.format(sender.id, receiver.id, receiver.id, sender.id))

                all_msgs = cursor.fetchall()

                all_msgs = all_msgs[msg_present:]

                for i in range(len(all_msgs)):
                    all_msgs[i] = list(all_msgs[i])
                    sender = User.objects.get(id = all_msgs[i][4])
                    receiver = User.objects.get(id = all_msgs[i][3])
                    all_msgs[i][1] = decode(generate_code(sender, receiver), all_msgs[i][1])

                
                output['all_msgs'] = all_msgs
                output['status'] = True
                return JsonResponse(output)
                # return GOOD

            except:
                output['status'] = False
                return JsonResponse(output)


    else:
        output['status'] = False
        return JsonResponse(output)

# get all deliveries
def getDeliveries(request):
    output = {}
    if request.method == "GET":
        if request.is_ajax():
            order_id = request.GET['order_id']
            print(order_id)
            output['order_id'] = order_id

            particular_order = order.objects.get(id = int(order_id))

            output['isCompleted'] = (particular_order.order_status == "COMPLETED")

            all_deliveries_container = []
            
            # Solution 1 starts
            
            cursor = connection.cursor()
            cursor.execute('''
            
                SELECT revised_file, order_date_time 
                FROM application_deliveries 
                WHERE order_id={}

                '''.format(int(order_id)))

            data = cursor.fetchall()
            print(data)

            # solution 1 ends

            # to get meaningfull datetime

            for i in data:
                print(i)
                myFile = i[0]
                actual_date = i[1].strftime("%d %b, %Y - %H:%M %p")
                all_deliveries_container.append((myFile, actual_date))

            output['all_deliveries'] = all_deliveries_container

    return JsonResponse(output)

# main page
def profile(request):
    if not request.user.is_authenticated:
        return redirect("index")

    context = {
        'date_joined': request.user.date_joined.date(),
    }

    if native_speaker.objects.filter(which_user = request.user).exists():
        if native_speaker.objects.get(which_user = request.user).isAccepted:
            context['status'] = "You are a native speaker"
            context['AS'] = 'SPEAKER'
            itsNativeSpeaker = native_speaker.objects.get(which_user = request.user)

            if order.objects.filter(alloted_to = itsNativeSpeaker).exists():
                context['orders'] = order.objects.filter(alloted_to = itsNativeSpeaker).order_by("-id")
                
        else:
            context['status'] = "Native speaker request has been sent"
    else:
        context['AS'] = 'USER'
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

