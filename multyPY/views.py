from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.shortcuts import redirect
from datetime import datetime, timezone

from django.views import generic
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from multyPY.models import *
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncDate,TruncHour
import json
from django.core.serializers.json import DjangoJSONEncoder

import random
import string
from django.core import serializers

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

@login_required
@csrf_protect
def exam(request, base_number):
    if request.method == "POST":
        answers=[]
        exam = Exam(base_number=base_number, user=request.user)
        exam.save()
        correct_answers=0
        for i in range(1,11):
            answer=int(request.POST.get('quantity{base_number}_{multiplier}'.format(base_number = base_number, multiplier = i),0))
            correct=answer==base_number*i
            examAnswer = ExamAnswer(multiplier=i,answer=answer,correct=correct,exam=exam)
            examAnswer.save()
            if correct:correct_answers+=1;
        if correct_answers==10:
            pass_message='Flawless'
        elif correct_answers>=9:
            pass_message='Greate Job'
        elif correct_answers>=8:
            pass_message='Very Good'
        elif correct_answers>=7:
            pass_message='Good Job'
        elif correct_answers>=5:
            pass_message='You have passed'
        else:
            pass_message='You didnt pass'

        if correct_answers>=5:
            if base_number<10:
                permission = Permission.objects.get(
                    codename='canExamBase_number'+str(base_number+1),
                    content_type=ContentType.objects.get_for_model(Exam),
                )
                if not request.user.has_perm('multyPY.canExamBase_number'+str(base_number+1)):
                    print(correct_answers)
                    request.user.user_permissions.add(permission)
            else:
                permission = Permission.objects.get(
                    codename='canFinalExam',
                    content_type=ContentType.objects.get_for_model(FinalExam),
                )
                if not request.user.has_perm('multyPY.canFinalExam'):
                    print(correct_answers)
                    request.user.user_permissions.add(permission)
                request.user.save()
        exam.number_of_correct=correct_answers
        correct=correct_answers>=5
        exam.save()
        answers = ExamAnswer.objects.filter(exam=exam).order_by('multiplier')
        return render(request, 'multiplication_table_ex.html', {'base_number': base_number,'disabled':True,'correct':correct_answers>=5,'answers':answers,'pass_message':pass_message,'score':correct_answers,'helppage':23 if correct else 24})


    if request.user.has_perm('multyPY.canExamBase_number'+str(base_number)):
        return render(request, 'multiplication_table_ex.html', {'base_number': base_number,'disabled':False,'helppage':21})
    elif base_number==1:
        return redirect('home')
    else:
        return redirect('multiplication_table_ex' ,base_number= base_number-1)


@login_required
@csrf_protect
def exams(request):
    if request.user.has_perm('multyPY.canFinalExam'):
        if request.method == "POST":
            exam = FinalExam(user=request.user)
            exam.save()
            correct_answers=0
            for base_number in range(1,11):
                examTable = FinalExamTable(base_number=base_number,examTable=exam)
                examTable.save()
                for multiplier in range(1,11):
                    answer=int(request.POST.get('quantity{base_number}_{multiplier}'.format(base_number = base_number, multiplier = multiplier),0))
                    correct=answer==base_number*multiplier
                    examAnswer = FinalExamAnswer(multiplier=multiplier,answer=answer,correct=correct,finalExamTablexamTable=examTable)
                    examAnswer.save()

                    if correct:correct_answers+=1;
            if correct_answers==100:
                pass_message='Flawless'
            elif correct_answers>=90:
                pass_message='Greate Job'
            elif correct_answers>=80:
                pass_message='Very Good'
            elif correct_answers>=70:
                pass_message='Good Job'
            elif correct_answers>=50:
                pass_message='You have passed'
            else:
                pass_message='You didnt pass'
            correct=correct_answers>=50
            examTable.number_of_correct=correct_answers
            examTable.save()
            examsQ = FinalExamTable.objects.filter(examTable=exam).order_by('base_number')
            exams=[]
            for exam in examsQ.values('base_number','id'):
                base_number=exam['base_number']
                answers = FinalExamAnswer.objects.filter(finalExamTablexamTable_id=exam['id']).order_by('finalExamTablexamTable__base_number','multiplier')
                exams.append({'answers':answers,'base_number':base_number,'id':exam['id']})
            return render(request, 'multiplication_tables_ex.html', {'base_number': base_number,'exams':exams,'disabled':True,'correct':correct,'pass_message':pass_message,'score':correct_answers,'helppage':23 if correct else 24})
        return render(request, 'multiplication_tables_ex.html',{'helppage':21} )
    return redirect('home')
@login_required
@csrf_protect
def multiple_choice(request, base_number=random.randint(1,10),multiplier=random.randint(1,10),num_of_option=5,tr=False):
    print(request.session.session_key)
    print(request.user.id)
    if request.method == "POST":
        base_number = int(request.POST["base_number"])
        multiplier = int(request.POST["multiplier"])
        options = json.loads(request.POST['options'])

        num_of_option=len(options)
        answer = int(request.POST["answer"])
        correct_answer=base_number*multiplier
        correct = correct_answer==answer
        question, created = Question.objects.get_or_create(base_number=base_number, multiplier=multiplier,options=str(options))
        answer_obj = Answer(answer=answer,question=question,user=request.user,correct=correct)

        answer_obj.save()
        print(question, created,answer,answer_obj.id,answer_obj.is_correct())
        return render(request, 'multiple_choice.html', {'base_number':base_number,'multiplier':multiplier,'options':options,'disabled':True,'checked_answer':answer,'correct':correct,'random':tr,'helppage':20 if correct else 19})
    else:
        options=[]
        correct_answer=base_number*multiplier
        while len(options)<num_of_option:
            r=random.randint(0,10*base_number*2)
            if r not in options and r != correct_answer:
                options.append(r)
        options[random.randint(0,num_of_option-1)]=correct_answer
        question, created = Question.objects.get_or_create(base_number=base_number, multiplier=multiplier,options=str(options))
        print(question, created)
        return render(request, 'multiple_choice.html', {'base_number':base_number,'multiplier':multiplier,'options':options,'disabled':False,'random':tr,'helppage':18})

@login_required
@csrf_protect
def multiple_choice_r(request,base_number):
    return multiple_choice(request, base_number,random.randint(1,10),5,False)

@login_required
@csrf_protect
def multiple_choice_tr(request):
    return multiple_choice(request, random.randint(1,10),random.randint(1,10),5,True)

@login_required
def answers(request):
    user=request.user
    answers = Answer.objects.filter(user=user).order_by('question__base_number','question__multiplier')

    return render(request, 'answers.html', {'answers':answers,'view':False})


def view_answers(request,username):
    user=request.user
    if user.groups.filter(name = 'teacher').exists():
        tuser=User.objects.get(username=username)
        if tuser:
            answers = Answer.objects.filter(user=tuser).order_by('question__base_number','question__multiplier')
            return render(request, 'answers.html', {'answers':answers,'view':True,'username':username,'helppage':11})
    return HttpResponseRedirect(reverse('students'))

def view_exam_answers(request,username):
    user=request.user
    if user.groups.filter(name = 'teacher').exists():
        tuser=User.objects.get(username=username)
        if tuser:
            examsQ = Exam.objects.filter(user=tuser).values('base_number','id').order_by('date','base_number','number_of_correct')

            exams=[]
            for exam in examsQ:
                base_number=exam['base_number']
                answers = ExamAnswer.objects.filter(exam_id=exam['id']).order_by('exam__base_number','multiplier')
                exams.append({'answers':answers,'base_number':base_number,'id':exam['id']})
            return render(request, 'exam_answers.html', {'exams':exams,'view':True,'username':username,'helppage':11})
    return HttpResponseRedirect(reverse('students'))
def view_final_exam_answers(request,username):
    user=request.user
    if user.groups.filter(name = 'teacher').exists():
        tuser=User.objects.get(username=username)
        if tuser:
            finalExamsQ =FinalExam.objects.filter(user=tuser)
            finalExams=[]
            for finalExam in finalExamsQ:
                examsQ = FinalExamTable.objects.filter(examTable=finalExam).order_by('base_number')
                exams=[]
                for exam in examsQ.values('base_number','id'):
                    base_number=exam['base_number']
                    answers = FinalExamAnswer.objects.filter(finalExamTablexamTable_id=exam['id']).order_by('finalExamTablexamTable__base_number','multiplier')
                    exams.append({'answers':answers,'base_number':base_number,'id':exam['id']})
                if exams:
                    finalExams.append({'exams':exams,'id':finalExam.id})
                else:
                    examsQ.delete()
            return render(request, 'final_exam_answers.html', {'finalExams':finalExams,'view':True,'username':username})
    return HttpResponseRedirect(reverse('students'))
@login_required
def students(request):
    if not request.user.groups.filter(name = 'teacher').exists():
        return HttpResponseRedirect(reverse('home'))
    users=User.objects.filter(groups__name='student').values('username')
    return render(request,'students.html',{'students':[user['username'] for user in users],'helppage':9})
@login_required
def view_profile(request,username):
    if not request.user.groups.filter(name = 'teacher').exists():
        return HttpResponseRedirect(reverse('home'))
    tuser=User.objects.get(username=username)
    if tuser:
        return render(request, 'registration/profile.html',{'view':True,'username':username,'helppage':10})
    return HttpResponseRedirect(reverse('students'))

#not secure maybe ?
@login_required
def edit_permitions(request,username):
    if not request.user.groups.filter(name = 'teacher').exists():
        return HttpResponseRedirect(reverse('home'))
    tuser=User.objects.get(username=username)
    if tuser:
        if request.method == "POST":
            permissionID = int(request.POST.get('permissionID'))
            permission = Permission.objects.get(id=permissionID)
            if request.user.has_perm('multyPY.'+permission.codename):


                print(permission)
                if tuser.has_perm('multyPY.'+permission.codename):
                    tuser.user_permissions.remove(permission)
                else:
                    tuser.user_permissions.add(permission)
        userpermissions = Permission.objects.filter(user=tuser).values('id','name')

        allpermissions = Permission.objects.filter(Q(codename__contains='canExamBase_number')|Q(codename__contains='canFinalExam')).values('id','name')
        allpermissions =[perm for perm in allpermissions if not perm in userpermissions]
        return render(request,'edit_permitions.html',{'username':username,'userpermissions':userpermissions,'allpermissions':allpermissions,'helppage':12})

    return HttpResponseRedirect(reverse('students'))
@login_required
def keycodes(request):
    if not request.user.groups.filter(name = 'teacher').exists():
        return HttpResponseRedirect(reverse('home'))
    if request.method == "POST":
        keyID=request.POST.get('keyID')
        if keyID:
            StudentKey.objects.get(id=keyID).delete()
        else:
            StudentKey(key=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))).save()
    keycodes= StudentKey.objects.filter()
    return render(request,'keycodes.html',{'keycodes':keycodes,'helppage':13})

def home(request):
    return render(request, 'home.html',{'helppage':5})


def get_total_progres_per_time(query_set):
    plot_data={}
    prev=0
    plot_data['x']=[]
    plot_data['y']=[]
    for t in query_set:
        plot_data['x'].append(t['date'].strftime('%Y-%m-%d %H:%M:%S'))
        prev+=1
        plot_data['y'].append(prev)
    plot_data['x'].append((datetime.now()).strftime('%Y-%m-%d %H:%M:%S'))
    plot_data['y'].append(prev)

    return plot_data
@login_required
def json_test(request):

    return JsonResponse(get_progress_of_multiple_choice(request),safe=False)

@login_required
def json_progress_top_exam(request):
    user=request.user
    if request.GET.get('user') and user.groups.filter(name = 'teacher').exists():
        tuser=User.objects.get(username=request.GET['user'])
        if tuser:
            user=tuser
    correct_plot_data={}
    correct_plot_data['y']=[]
    correct_plot_data['x']=[]
    wrong_plot_data={}
    wrong_plot_data['y']=[]
    wrong_plot_data['x']=[]
    for i in range(1,11):
        answers = Exam.objects.filter(user=user,base_number=i).order_by('-number_of_correct').values('number_of_correct')
        if len(answers)>0:
            number_of_correct = answers[0]['number_of_correct']

            correct_plot_data['x'].append('table of '+str(i))
            correct_plot_data['y'].append((number_of_correct)*10)

            wrong_plot_data['x'].append('table of '+str(i))
            wrong_plot_data['y'].append((10-number_of_correct)*10)

    correct_plot_data['name']='% Correct Answers'
    correct_plot_data['color']='rgb(0,128,0)'
    wrong_plot_data['name']='% Wrong Answers'
    wrong_plot_data['color']='rgb(128,0,0)'
    finals = FinalExam.objects.filter(user=request.user)
    if len(finals)>0:
        c=[]
        for final in finals:
            exams = FinalExamTable.objects.filter(examTable=final)
            prev=0;
            for exam in exams:

                answers = FinalExamAnswer.objects.filter(finalExamTablexamTable=exam).values('correct')
                for answer in answers:
                    if answer['correct']:prev+=1;
            c.append(prev)
        c.sort(reverse = True)
        correct_plot_data['x'].append('Final Exam')
        correct_plot_data['y'].append(c[0])

        wrong_plot_data['x'].append('Final Exam')
        wrong_plot_data['y'].append(100-c[0])

    return JsonResponse([correct_plot_data,wrong_plot_data],safe=False)
@login_required
def json_progress_total_exam(request):
    user=request.user
    print(user)
    if request.GET.get('user') and user.groups.filter(name = 'teacher').exists():
        tuser=User.objects.get(username=request.GET['user'])
        if tuser:
            user=tuser
    correct_plot_data={}
    correct_plot_data['y']=[]
    correct_plot_data['x']=[]
    wrong_plot_data={}
    wrong_plot_data['y']=[]
    wrong_plot_data['x']=[]
    total_plot_data={}
    total_plot_data['y']=[]
    total_plot_data['x']=[]

    answers = Exam.objects.filter(user=user).order_by('date').values('date','number_of_correct')
    prev_correct=0
    prev_wrong=0
    for answer in answers:
        number_of_correct = answer['number_of_correct']
        date=answer['date'].strftime('%Y-%m-%d %H:%M:%S')
        correct_plot_data['x'].append(date)
        prev_correct+=number_of_correct
        correct_plot_data['y'].append(prev_correct)

        wrong_plot_data['x'].append(date)
        prev_wrong+=10-number_of_correct
        wrong_plot_data['y'].append(prev_wrong)

    correct_plot_data['name']='Total Correct Answers'
    correct_plot_data['color']='rgb(0,128,0)'
    correct_plot_data['fill']='tozeroy'
    wrong_plot_data['name']='Total Wrong Answers'
    wrong_plot_data['color']='rgb(128,0,0)'
    wrong_plot_data['fill']='tozeroy'
    correct_plot_data['x'].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    wrong_plot_data['x'].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    correct_plot_data['y'].append(prev_correct)
    wrong_plot_data['y'].append(prev_wrong)
    return JsonResponse([correct_plot_data,wrong_plot_data],safe=False)

def get_progress_of_multiple_choice(request):
    user=request.user
    if request.GET.get('user') and user.groups.filter(name = 'teacher').exists():
        tuser=User.objects.get(username=request.GET['user'])
        if tuser:
            user=tuser
    correct_plot_data={}
    correct_plot_data['y']=[]
    correct_plot_data['x']=[]
    wrong_plot_data={}
    wrong_plot_data['y']=[]
    wrong_plot_data['x']=[]

    correct_plot_data['name']='Total Correct Answers'
    correct_plot_data['color']='rgb(0,128,0)'
    correct_plot_data['fill']='tozeroy'
    wrong_plot_data['name']='Total Wrong Answers'
    wrong_plot_data['color']='rgb(128,0,0)'
    wrong_plot_data['fill']='tozeroy'
    prev_correct=0
    prev_wrong=0
    answers = Answer.objects.filter(user=user).order_by('date').values('date','correct')
    for answer in answers:
        correct_plot_data['x'].append(answer['date'].strftime('%Y-%m-%d %H:%M:%S'))
        wrong_plot_data['x'].append(answer['date'].strftime('%Y-%m-%d %H:%M:%S'))
        if answer['correct']:
            prev_correct+=1
        else:
            prev_wrong+=1
        correct_plot_data['y'].append(prev_correct)
        wrong_plot_data['y'].append(prev_wrong)
    correct_plot_data['x'].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    wrong_plot_data['x'].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    correct_plot_data['y'].append(prev_correct)
    wrong_plot_data['y'].append(prev_wrong)
    return [correct_plot_data,wrong_plot_data]
@login_required

def ac_profile(request):
    return render(request, 'registration/profile.html',{'helppage':15})
def multiplication_tables(request):
    return render(request, 'multiplication_tables.html',{'helppage':16})
def multiplication_table(request,base_number):
    return render(request, 'multiplication_table.html',{'base_number':base_number,'helppage':16})
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
@csrf_protect
def login_view(request):
    print(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'registration/login.html',{'login':{'errors':["Your account was inactive"]},'helppage':8})

        else:
            return render(request, 'registration/login.html',{'login':{'errors':["Invalid login details given"]},'helppage':8})
    else:
        return render(request, 'registration/login.html',{'helppage':8})
@csrf_protect
def register(request):
    context={'helppage':7}
    form = UserCreationForm(request.POST or None)
    context['form']=form
    role = request.POST.get('role',None)
    key = request.POST.get('key',None)
    form.is_valid()
    context['form']=form
    context['key']={'errors':[]}
    print(context)
    if request.method == "POST":
        if not role in ['teacher','student']:
            return render(request,'registration/register.html',context)
        if role == 'teacher':
            if not TeacherKey.objects.filter(key=key).exists():
                context['key']['errors'].append("key doesn't exist")
                return render(request,'registration/register.html',context)
        elif role == 'student':
            if not StudentKey.objects.filter(key=key).exists():
                context['key']['errors'].append("key doesn't exist")
                return render(request,'registration/register.html',context)
        if form.is_valid():
            user = form.save()
            login(request,user)
            if role == 'teacher':
                TeacherKey.objects.filter(key=key).delete()
            else:
                StudentKey.objects.filter(key=key).delete()

            new_group, created = Group.objects.get_or_create(name=role)
            new_group.user_set.add(user)
            if role == 'teacher':
                tpermissions = Permission.objects.filter(
                    content_type=ContentType.objects.get_for_model(Exam),
                )
                epermission = Permission.objects.get(
                    codename='canFinalExam',
                    content_type=ContentType.objects.get_for_model(FinalExam),
                )
                user.user_permissions.set(tpermissions)
                user.user_permissions.add(epermission)
            else:
                permission = Permission.objects.get(
                    codename='canExamBase_number1',
                    content_type=ContentType.objects.get_for_model(Exam),
                )

                user.user_permissions.add(permission)
            return HttpResponseRedirect(reverse('home'))

    return render(request,'registration/register.html',context)
def helppage(request,helppage):
    return render(request,'help_pdf.html',{'page':helppage})
