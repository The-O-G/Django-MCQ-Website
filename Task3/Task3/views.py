from http.client import HTTPResponse
from re import A
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from Task3.models import Info

# So the number of questions solely relies on the amount of Questions in "Ques" list.
# Please add the titles, options as well as the solutions in c_answers.

titles = ['1','2','3','4']
Ques = ['11.1','22','33','44']
options = [['1','2','3','4'],
           ['5','6','7','8'],
           ['9','0','1','2'],
           ['3','4','5','6'],
            ]
question_number = 0
answered = {}
points = 0
c_answers = ['a','a','a','a']
userid = ''
def signin(request):
    return render(request, 'Signin.html')

def firstpage(request):

    return render(request, 'Signin.html')

def checklogin(request):
    return render(request, 'register.html')

def registration(request):
    global userid
    userid = request.POST.get('Userid')
    fname_ = request.POST.get('fname')
    lname_ = request.POST.get('lname')
    email_ = request.POST.get('email')
    female = request.POST.get('Female')
    male = request.POST.get('Male')
    phone_num = request.POST.get('phone')
    psw = request.POST.get('psw')
    is_user = User.objects.filter(username = userid).exists()
    gndr = ''
    if male=='on':
        gndr = 'M'
    elif female=='on':
        gndr = 'F'
    else:
        gndr = 'U'
    if is_user:
        return render(request,'register.html',{"response":"Already a user please sign in"})

    else:
        User.objects.create(username = userid, password = psw)
        user = User.objects.get(username = userid)
        post = Info(
            name = userid, 
            fname = fname_,
            lname= lname_,
            email= email_,     
            phone= int(phone_num), 
            gender = gndr,
            author = user
            )
        post.save()
        return render(request,'register.html',{"response":"Registeration successful!! please login "})

def login(request):
    userid = request.POST.get('Userid')
    psw = request.POST.get('psw')
    if User.objects.filter(username = userid).exists() and psw == User.objects.get(username = userid).password:
        return render(request, 'rules_page.html')
    else:
        return render(request, 'Signin.html', {'message':'Please check User Id and password'})

def index(request):
    return render(request, 'rules_page.html')

def questions(request):
    # This is purely for the first question
    global points
    points = 0
    return render(request,
                  'question.html',
                  {'Title': titles[0],
                   'Q': Ques[0],
                   '1': options[0][0],
                   '2': options[0][1],
                   '3': options[0][2],
                   '4': options[0][3],
                   }
                  )

def quiz(request):
    # This is for all the other questions
    global question_number,points
    question_number+=1
    a = request.POST.get('a')
    b = request.POST.get('b')
    c = request.POST.get('c')
    d = request.POST.get('d')

    if a!=None:
        answered[question_number] = 'a'
        # print('a')
    elif b!=None:
        answered[question_number] = 'b'
        # print('b')
    elif c!=None:
        answered[question_number] = 'c'
        # print('c')
    elif d!=None:
        answered[question_number] = 'd'
        # print('d')

    if question_number<len(Ques):
        return render(request, 
                    'question.html',
                    {'Title': titles[question_number],
                    'Q': Ques[question_number],
                    'a': options[question_number][0],
                    'b': options[question_number][1],
                    'c': options[question_number][2],
                    'd': options[question_number][3],
                    })
    else:
        global userid
        question_number=0
        for q in range(1,1+len(Ques)):
            if answered[q] == c_answers[q-1]:
                points+=1
        print('-'*10)
        print(userid)
        print('-'*10)
        # m = Info.objects.get(name = userid)
        # m.score = points
        # m.save()
        return render(request,'Result.html',{'Score':f'{points}'})
