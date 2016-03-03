from reportlab.pdfgen import canvas
from cStringIO import StringIO
from django.http import HttpResponse,Http404,HttpResponseRedirect
# from django.shortcuts import render,get_object_or_404
# from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as lgin
from django.shortcuts import render,redirect
from django.contrib.auth import logout as lgout
from django.core.exceptions import ObjectDoesNotExist
# from django.template.loader import get_template
#from email.mime import MIMEText
# from django.core.exceptions import ObjectDoesNotExist
# from django.db import connection
# from django.core.mail import send_mail
from .forms import UserForm, UserProfileForm, ImageForm
from .models import UserDetails1,UserDetails2,User
import smtplib
import pdf
import os
import string
#from wkhtmltopdf.views import PDFTemplateResponse
import random
#from xhtml2pdf import pisa
globals()
# Create your views here.

def index(request):
    return render(request,'index.html',{})

def handle_uploaded_file(f,us,ty=1):
    destination = open(os.path.dirname(os.path.dirname(__file__))+'/static/images/uploads/'+str(ty)+str(us)+'.jpg','wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    return
class Gmail(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)        
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session
	
    def send_message(self, receivers,subject, body):
        ''' This must be removed '''
        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + self.email,
            "MIME-Version: 1.0",
           "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            receivers,
            headers + "\r\n\r\n" + body)

def register(request):
    print request
    if not request.user.is_authenticated():
        context = RequestContext(request)
        registered = False
        if request.method == 'POST':
            if User.objects.filter(email=request.POST[u'email']):
                return HttpResponseRedirect('/register/registered/')
            f = open('users.txt','r')
            lola = f.readline().strip('\n')
            f.close()
            #gmail = Gmail('','')# change this
            #gmail.send_message(request.POST['email'],'PhD Admissions 2015 Registration successful',"Dear Candidate,<br>Your registration has been successfully done in our admission portal. Following are the login credentials :<br>Username : <b>H"+str(lola) + "</b><br>Password : <b>"+ request.POST['password']+'</b><br><a href="14.139.41.172:8090/register/login/">Click here</a> to login and submit the application form.<br>Please do not reply to this mail<br>Best wishes,<br>PG Admission 2015<br>2015')
            f = open('users.txt','w')
            lol = int(lola) + 1
            f.write(str(lol))
            f.close()
            request.POST[u'username'] = unicode(lola)
            user_form = UserForm(data=request.POST)
            profile_form = UserProfileForm(data=request.POST)
            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                t1= UserDetails1(user=user,email=request.POST['email'])
                t2= UserDetails2(user=user,email=request.POST['email'])

                t1.save()
                t1.application_id=user.username
                t1.full_name = request.POST['full_name']
                t1.father_name = request.POST['father_name']
                t1.mother_name = request.POST['mother_name']
                t1.dob = request.POST['dob']
                t1.gender = request.POST['gender']
                t1.nation = request.POST['nation']
                t1.category = request.POST['category']
                t1.phys = request.POST['phys']
                t1.mobile = request.POST['mobile']
                t1.perma_addr = request.POST['perma_addr']
                t1.corres_addr = request.POST['corres_addr']
                t1.save()

                t2.save()
                t2.application_id=user.username
                t2.full_name = request.POST['full_name']
                t2.father_name = request.POST['father_name']
                t2.mother_name = request.POST['mother_name']
                t2.dob = request.POST['dob']
                t2.gender = request.POST['gender']
                t2.nation = request.POST['nation']
                t2.category = request.POST['category']
                t2.phys = request.POST['phys']
                t2.mobile = request.POST['mobile']
                t2.perma_addr = request.POST['perma_addr']
                t2.corres_addr = request.POST['corres_addr']
                t2.save()
                #profile = profile_form.save(commit=False)
                #profile.user = user
                #profile.save()
                registered = True
                image_form = ImageForm(request.POST,request.FILES)

                print "h1"
                return render(request,'register/login.html',{'message':'You are successfully registered ,Please check for email with login credentials!','image_form':image_form})
            else:
                print user_form.errors,
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()
            return render(request,'register/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered},context)
    else:
        return HttpResponseRedirect('/register/loggedin')

def loggedin(request):
    return render(request,'register/loggedin.html',{})
def registered(request):
    return render(request,'register/registered.html',{})
def prg(request):
    return render(request,'register/program.html',{})

def select_prg(request):
    if request.method == 'POST':
        prg = request.POST['prg']
        if prg == 'Phd Program':
	        return HttpResponseRedirect('/register/phd/')
	if prg == 'PG Program':
		return HttpResponseRedirect('/register/pg/')
	if prg == 'null':
		return render(request,'register/program.html',{})

def change_pass(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.filter(email=email)[User.objects.filter(email=email).count() - 1]
        except:
            return HttpResponse("Email Id is not registered")
        user_name = user.username
        gmail = Gmail('user','pass')#change this
        passcode = ''.join(random.choice(string.ascii_uppercase) for i in range(5))
        gmail.send_message(email,"Change Password IIT PORTAL","Your new password is <b>"+passcode+'</b>'+"with registered Username : <b>"+user_name+'</b>')
        user.set_password(passcode)
        user.save()
        return HttpResponse("You new password is sent to your registered Email ID")
    else:
        return render(request,'register/change_pass.html',{})

def login(request):
    
    if not request.user.is_authenticated():
        if request.method == 'POST':
                username = request.POST['username']
                try:
                    user = User.objects.get(username=username)
                    user1 = UserDetails1.objects.get(application_id=username)
                except:
                    return HttpResponse("User doesn't exist <a href='/register/login/'>Retry</a>")
                passcode = request.POST['password']
                print "login post"

                if user.check_password(passcode):
                    user = authenticate(username=username,password=passcode)
                    lgin(request,user)
                    image_form=ImageForm(request.POST,request.FILES)
                    print "correct"
                    #request.session[]
                    request.session['user']=username
                    image_url="/static/images/uploads/1"+user1.full_name+".jpg"

                    sign_url="/static/images/uploads/2"+user1.full_name+".jpg"
                    return render(request,'register/upload_image.html',{'image_form':image_form,'username':username,'password':passcode,'user':user,'form_data':user,'image_url':image_url,'sign_url':sign_url})
                    #return HttpResponseRedirect('/register/part_form/')
                else:
                    return HttpResponse("Wrong password <a href='/register/login/'>Retry</a>")
        else:

            image_form=ImageForm(request.POST,request.FILES)
            return render(request,'register/login.html',{'image_form':image_form})
    else:
        flag=False
        if request.method == 'POST':
            flag=request.session.get('flag')
            if not flag:
                username=request.user
                try:
                    user = UserDetails1.objects.get(application_id=username)
                    user2 = UserDetails2.objects.get(application_id=username)
                except:
                    return HttpResponse("User doesn't exist <a href='/register/login/'>Retry</a>")

                if('image' in request.FILES):
                    user.image= request.FILES['image']
                    user2.image= request.FILES['image']
                    
                    handle_uploaded_file(user.image,user.full_name,1)
                    print "imaaagw"

                if('signature' in request.FILES):
                    user.signature= request.FILES['signature']
                    user2.signature= request.FILES['signature']
                    
                    handle_uploaded_file(user.signature,user.full_name,2)
                    print "imaaagw"
                image_form=ImageForm(request.POST,request.FILES)
                image_url="/static/images/uploads/1"+user.full_name+".jpg"
                
                sign_url="/static/images/uploads/2"+user.full_name+".jpg"
                print "correct"
                            #request.session[]
                return render(request,'register/upload_image.html',{'image_form':image_form,'username':username,'user':user,'image_url':image_url,'sign_url':sign_url})
               
        return HttpResponseRedirect('/register/form/')


def registrationForm(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            user_name = UserDetails1.objects.get(user=request.user)
            if user_name.submitt == "n":
                return HttpResponse('You have submitted this part of the form Go to <a href="/register/part_form/">Next Part</a>')
            #return HttpResponse("Something went wrong")
            if 'save' in request.POST:
                user_name.full_name = request.POST['full_name']
                user_name.father_name = request.POST['father_name']
                user_name.mother_name = request.POST['mother_name']
                user_name.dob = request.POST['dob']
                user_name.gender = request.POST['gender']
                user_name.nation = request.POST['nation']
                user_name.category = request.POST['category']
                user_name.phys = request.POST['phys']
                user_name.mobile = request.POST['mobile']
                user_name.perma_addr = request.POST['perma_addr']
                user_name.corres_addr = request.POST['corres_addr']
                user_name.save()
                #return HttpResponse("Form Saved You can go <a href='/register/form/'>Back</a> and Submit the form after review")
            if 'submit' in request.POST:
                user_name.full_name = request.POST['full_name']
                user_name.father_name = request.POST['father_name']
                user_name.mother_name = request.POST['mother_name']
                user_name.dob = request.POST['dob']
                user_name.gender = request.POST['gender']
                user_name.nation = request.POST['nation']
                user_name.category = request.POST['category']
                user_name.phys = request.POST['phys']
                user_name.mobile = request.POST['mobile']
                user_name.perma_addr = request.POST['perma_addr']
                user_name.corres_addr = request.POST['corres_addr']
                user_name.submitt = "Y"
                user_name.save()
                #return HttpResponse("Form Submitted go for the <a href='/register/part_form/'>Second Part</a> of the form   ")
        else:
            user_name = UserDetails1.objects.get(user=request.user)
            #if user_name.submitt == "N":
             #   return HttpResponseRedirect('/register/phd/')
                #return HttpResponse('You have submitted this part of the form Go to <a href="/register/part_form/">Next Part</a>')
            return render(request,'registration1.html',{'form_data':user_name})
    else:

        return HttpResponseRedirect('/register/login/')

#def forom(request):
def phd(request):
    if request.user.is_authenticated():
        user_name = UserDetails1.objects.get(user=request.user)
        #if user_name.registered == "Y":
         #   return HttpResponseRedirect('/register/view_form/')

        if request.method == 'POST':
            image_form = ImageForm(request.POST,request.FILES)

            if image_form.is_valid():
                handle_uploaded_file(request.FILES['image'],user_name.full_name,1)
                handle_uploaded_file(request.FILES['signature'],user_name.full_name,2)
                handle_uploaded_file(request.FILES['score_card'],user_name.full_name,3)

            user_name = UserDetails1.objects.get(user=request.user)
            if 'save' in request.POST:
                #user_name = UserDetails1.objects.get(user=request.user)
                #handle_uploaded_file(request.FILES['image'])
                print request.FILES
                if('image' in request.FILES):
                    user_name.image= request.FILES['image']

                if('signature' in request.FILES):
                    user_name.signature = request.FILES['signature']
                if('score_card' in request.FILES):
                    user_name.signature = request.FILES['score_card']

                user_name.ereceipt = request.POST['ereceipt']
                user_name.dop = request.POST['dop']

                user_name.std_status = request.POST['std_status']
                user_name.fin_status = request.POST['fin_status']

                user_name.disc_choice1 = request.POST['dept1']
                if(user_name.disc_choice1=='Department of Electrical Engineering'):
                    user_name.spec_choice1 = request.POST['disc11']
                elif(user_name.disc_choice1=='Department of Mechanical Engineering'):
                    user_name.spec_choice1 = request.POST['disc12']
                user_name.choice_prg2 = request.POST['choice_dept2']
                user_name.disc_choice2 = request.POST['dept2']
                if(user_name.disc_choice2=='Department of Electrical Engineering'):
                    user_name.spec_choice2 = request.POST['disc21']
                elif(user_name.disc_choice2=='Department of Mechanical Engineering'):
                    user_name.spec_choice2 = request.POST['disc22']
                user_name.choice_prg3 = request.POST['choice_dept3']
                user_name.disc_choice3 = request.POST['dept3']
                if(user_name.disc_choice3=='Department of Electrical Engineering'):
                    user_name.spec_choice3 = request.POST['disc31']
                elif(user_name.disc_choice3=='Department of Mechanical Engineering'):
                    user_name.spec_choice3 = request.POST['disc32']

                user_name.gatestatus = request.POST['gatestatus']
                if(user_name.gatestatus=='Gate/GPAT Qualified'):
                    user_name.gate_exam = request.POST['gate_exam']
                    user_name.gate_roll = request.POST['gate_roll']
                    user_name.gate_year = request.POST['gate_year']
                    user_name.gate_disc = request.POST['gate_disc']
                    user_name.gate_rank = request.POST['gate_rank']
                    user_name.gate_score = request.POST['gate_score']
                    #user_name.score_card = request.FILES['score_card']
                if(user_name.gatestatus=='UGC-CSIR-NET Qualified'):
                    user_name.gate_exam = request.POST['net_exam']
                    user_name.gate_roll = request.POST['net_roll']
                    user_name.gate_year = request.POST['net_year']
                    user_name.gate_disc = request.POST['net_disc']
                    user_name.gate_rank = request.POST['net_rank']
                    user_name.gate_score = request.POST['net_score']
                if(user_name.gatestatus=='Other External Fellowships'):
                    user_name.detail_scholar=request.POST['detail_scholar']

                user_name.status_deg = request.POST['status_deg']
                user_name.quali_degree = request.POST['quali_degree']
                user_name.degree_name = request.POST['degree_name']
                user_name.univ_name = request.POST['univ_name']
                user_name.degree_disc = request.POST['degree_disc']
                user_name.year_passing = request.POST['year_passing']
                user_name.aggre_per = request.POST['aggre_per']


                user_name.inter_cert_name = request.POST['inter_cert_name']
                user_name.inter_board_name = request.POST['inter_board_name']
                user_name.inter_sub = request.POST['inter_sub']
                user_name.inter_year_passing = request.POST['inter_year_passing']
                user_name.inter_aggre_per = request.POST['inter_aggre_per']

                user_name.high_cert_name = request.POST['high_cert_name']
                user_name.high_board_name = request.POST['high_board_name']
                user_name.high_sub = request.POST['high_sub']
                user_name.high_year_passing = request.POST['high_year_passing']
                user_name.high_aggre_per = request.POST['high_aggre_per']

                user_name.work_exp = request.POST['work_exp']
                print user_name.work_exp
                user_name.period_from = request.POST['period_from']
                user_name.period_to = request.POST['period_to']
                user_name.work_org = request.POST['work_org']
                user_name.position = request.POST['position']

                user_name.publica_status = request.POST['publica_status']
                user_name.publica = request.POST['publica']

                user_name.refree1_name = request.POST['refree1_name']
                user_name.refree2_name = request.POST['refree2_name']
                user_name.refree1_email = request.POST['refree1_email']
                user_name.refree2_email = request.POST['refree2_email']

                user_name.save()
                return render(request,'registration1.html',{'user_data':user_name,'image_form':image_form,'form_data':user_name})

            if 'submit' in request.POST:
                user_name.ereceipt = request.POST['ereceipt']
                if('image' in request.FILES):
                    user_name.image= request.FILES['image']

                if('signature' in request.FILES):
                    user_name.signature = request.FILES['signature']

                user_name.ereceipt = request.POST['ereceipt']
                user_name.dop = request.POST['dop']

                user_name.std_status = request.POST['std_status']
                user_name.fin_status = request.POST['fin_status']

                user_name.disc_choice1 = request.POST['dept1']
                if(user_name.disc_choice1=='Department of Electrical Engineering'):
                    user_name.spec_choice1 = request.POST['disc11']
                elif(user_name.disc_choice1=='Department of Mechanical Engineering'):
                    user_name.spec_choice1 = request.POST['disc12']

                user_name.disc_choice2 = request.POST['dept2']
                if(user_name.disc_choice2=='Department of Electrical Engineering'):
                    user_name.spec_choice2 = request.POST['disc21']
                elif(user_name.disc_choice2=='Department of Mechanical Engineering'):
                    user_name.spec_choice2 = request.POST['disc22']

                user_name.disc_choice3 = request.POST['dept3']
                if(user_name.disc_choice3=='Department of Electrical Engineering'):
                    user_name.spec_choice3 = request.POST['disc31']
                elif(user_name.disc_choice3=='Department of Mechanical Engineering'):
                    user_name.spec_choice3 = request.POST['disc32']

                user_name.gatestatus = request.POST['gatestatus']
                if(user_name.gatestatus=='Gate/GPAT Qualified'):
                    user_name.gate_exam = request.POST['gate_exam']
                    user_name.gate_roll = request.POST['gate_roll']
                    user_name.gate_year = request.POST['gate_year']
                    user_name.gate_disc = request.POST['gate_disc']
                    user_name.gate_rank = request.POST['gate_rank']
                    user_name.gate_score = request.POST['gate_score']
                    user_name.score_card = request.FILES['score_card']
                if(user_name.gatestatus=='UGC-CSIR-NET Qualified'):
                    user_name.gate_exam = request.POST['net_exam']
                    user_name.gate_roll = request.POST['net_roll']
                    user_name.gate_year = request.POST['net_year']
                    user_name.gate_disc = request.POST['net_disc']
                    user_name.gate_rank = request.POST['net_rank']
                    user_name.gate_score = request.POST['net_score']
                if(user_name.gatestatus=='Other External Fellowships'):
                    user_name.detail_scholar=request.POST['detail_scholar']

                user_name.status_deg = request.POST['status_deg']
                user_name.quali_degree = request.POST['quali_degree']
                user_name.degree_name = request.POST['degree_name']
                user_name.univ_name = request.POST['univ_name']
                user_name.degree_disc = request.POST['degree_disc']
                user_name.year_passing = request.POST['year_passing']
                user_name.aggre_per = request.POST['aggre_per']


                user_name.inter_cert_name = request.POST['inter_cert_name']
                user_name.inter_board_name = request.POST['inter_board_name']
                user_name.inter_sub = request.POST['inter_sub']
                user_name.inter_year_passing = request.POST['inter_year_passing']
                user_name.inter_aggre_per = request.POST['inter_aggre_per']

                user_name.high_cert_name = request.POST['high_cert_name']
                user_name.high_board_name = request.POST['high_board_name']
                user_name.high_sub = request.POST['high_sub']
                user_name.high_year_passing = request.POST['high_year_passing']
                user_name.high_aggre_per = request.POST['high_aggre_per']

                user_name.work_exp = request.POST['work_exp']
                user_name.period_from = request.POST['period_from']
                user_name.period_to = request.POST['period_to']
                user_name.work_org = request.POST['work_org']
                user_name.position = request.POST['position']

                user_name.publica_status = request.POST['publica_status']
                user_name.publica = request.POST['publica']

                user_name.refree1_name = request.POST['refree1_name']
                user_name.refree2_name = request.POST['refree2_name']
                user_name.refree1_email = request.POST['refree1_email']
                user_name.refree2_email = request.POST['refree2_email']

                user_name.save()
                #user_name.registered = "Y"
                generate_pdf(request)
                return HttpResponse("FormSubmitted")
        else:
            user_name = UserDetails1.objects.get(user=request.user)
            image_form = ImageForm()
            print "hello1321"
            #if user_name.registered == "Y":
             #    return HttpResponse('You have submitted this part of the form Go to <a href="/register/part_form/">Next Part</a>')
            return render(request,'registration1.html',{'form_data':user_name,'image_form':image_form,'user_data':user_name})
    else:
        print "from phd"
        return HttpResponseRedirect('/register/login/')

def pg(request):
    if request.user.is_authenticated():
        user_name = UserDetails2.objects.get(user=request.user)
        #if user_name.registered == "Y":
         #   return HttpResponseRedirect('/register/view_form/')
        if request.method == 'POST':
            image_form = ImageForm(request.POST,request.FILES)
            #if image_form.is_valid():
                #handle_uploaded_file(request.FILES['image'],request.user.username,1)
                #handle_uploaded_file(request.FILES['signature'],request.user.username,2)
                #handle_uploaded_file(request.FILES['score_card'],request.user.username,3)
            if 'save' in request.POST:
                user_name = UserDetails2.objects.get(user=request.user)
                #handle_uploaded_file(request.FILES['image'])
                #user_name.image= request.FILES['image']
                #user_name.signature = request.FILES['signature']
                user_name.amt = request.POST['amt']
                user_name.ereceipt = request.POST['ereceipt']
                user_name.dop = request.POST['dop']
                user_name.sstatus = request.POST['sstatus']
                user_name.fstatus = request.POST['fstatus']
                user_name.pg_program1 = request.POST['pg_program']
                user_name.dept1 = request.POST['dept1']
                user_name.disc11 = request.POST['disc11']
                user_name.disc12 = request.POST['disc12']
                user_name.disc13 = request.POST['disc13']
                user_name.disc14 = request.POST['disc14']
                user_name.pg_program2 = request.POST['pg_program2']
                user_name.dept2 = request.POST['dept2']
                user_name.disc21 = request.POST['disc21']
                user_name.disc22 = request.POST['disc22']
                user_name.disc23 = request.POST['disc23']
                user_name.disc24 = request.POST['disc24']
                user_name.pg_program3 = request.POST['pg_program3']
                user_name.dept3 = request.POST['dept3']
                user_name.disc31 = request.POST['disc31']
                user_name.disc32 = request.POST['disc32']
                user_name.disc33 = request.POST['disc33']
                user_name.disc34 = request.POST['disc34']
                user_name.gate_status = request.POST['gatestatus']
                if(user_name.gate_status=='Gate/GPAT Qualified'):
                    user_name.exam_name = request.POST['gate_exam']
                    user_name.roll_roll = request.POST['gate_roll']
                    user_name.exam_year = request.POST['gate_year']
                    user_name.exam_disc = request.POST['gate_disc']
                    user_name.exam_rank = request.POST['gate_rank']
                    user_name.exam_score = request.POST['gate_score']
                    #user_name.score_card = request.FILES['score_card']
                if(user_name.gate_status=='UGC-CSIR-NET Qualified'):
                    user_name.exam_name = request.POST['net_exam']
                    user_name.exam_roll = request.POST['net_roll']
                    user_name.exam_year = request.POST['net_year']
                    user_name.exam_disc = request.POST['net_disc']
                    user_name.exam_rank = request.POST['net_rank']
                    user_name.exam_score = request.POST['net_score']
                if(user_name.gate_status=='Other External Fellowships'):
                    user_name.detail_scholar=request.POST['detail_scholar']
                #user_name.score_card = request.FILES['score_card']
                user_name.degree = request.POST['degree']
                user_name.degree_status = request.POST['degree_status']
                user_name.degree_name = request.POST['dname']
                user_name.degree_uni = request.POST['uname']
                user_name.degree_disc = request.POST['ddisc']
                user_name.degree_year = request.POST['dyear']
                user_name.degree_score = request.POST['dscore']
                user_name.inter = request.POST['inter']
                user_name.inter_board = request.POST['inter_board']
                user_name.inter_subject = request.POST['inter_subject']
                user_name.inter_year = request.POST['inter_year']
                user_name.inter_score = request.POST['inter_score']
                user_name.high = request.POST['high']
                user_name.high_board = request.POST['high_board']
                user_name.high_subject = request.POST['high_subject']
                user_name.high_year = request.POST['high_year']
                user_name.high_score = request.POST['high_score']
                #user_name.work_exp = request.POST['work_exp']
                user_name.period_from = request.POST['period_from']
                user_name.period_to = request.POST['period_to']
                user_name.work_org = request.POST['work_org']
                user_name.position = request.POST['position']
                user_name.save()
                return render(request,'registration2.html',{'user_data':user_name,'image_form':image_form})
            if 'submit' in request.POST:
                user_name = UserDetails2.objects.get(user=request.user)
                #handle_uploaded_file(request.FILES['image'])
                #user_name.image= request.FILES['image']
                #user_name.signature = request.FILES['signature']
                user_name.amt = request.POST['amt']
                user_name.ereceipt = request.POST['ereceipt']
                user_name.dop = request.POST['dop']
                user_name.sstatus = request.POST['sstatus']
                user_name.fstatus = request.POST['fstatus']
                user_name.pg_program1 = request.POST['pg_program']
                user_name.dept1 = request.POST['dept1']
                user_name.disc11 = request.POST['disc11']
                user_name.disc12 = request.POST['disc12']
                user_name.disc13 = request.POST['disc13']
                user_name.disc14 = request.POST['disc14']
                user_name.pg_program_select1 = request.POST['pg_program_select1']
                user_name.pg_program2 = request.POST['pg_program2']
                user_name.dept2 = request.POST['dept2']
                user_name.disc21 = request.POST['disc21']
                user_name.disc22 = request.POST['disc22']
                user_name.disc23 = request.POST['disc23']
                user_name.disc24 = request.POST['disc24']
                user_name.pg_program_select2 = request.POST['pg_program_select2']
                user_name.pg_program3 = request.POST['pg_program3']
                user_name.dept3 = request.POST['dept3']
                user_name.disc31 = request.POST['disc31']
                user_name.disc32 = request.POST['disc32']
                user_name.disc33 = request.POST['disc33']
                user_name.disc34 = request.POST['disc34']
                user_name.gate_status = request.POST['gatestatus']
                if(user_name.gate_status=='Gate/GPAT Qualified'):
                    user_name.exam_name = request.POST['gate_exam']
                    user_name.roll_roll = request.POST['gate_roll']
                    user_name.exam_year = request.POST['gate_year']
                    user_name.exam_disc = request.POST['gate_disc']
                    user_name.exam_rank = request.POST['gate_rank']
                    user_name.exam_score = request.POST['gate_score']
                    #user_name.score_card = request.FILES['score_card']
                if(user_name.gate_status=='UGC-CSIR-NET Qualified'):
                    user_name.exam_name = request.POST['net_exam']
                    user_name.exam_roll = request.POST['net_roll']
                    user_name.exam_year = request.POST['net_year']
                    user_name.exam_disc = request.POST['net_disc']
                    user_name.exam_rank = request.POST['net_rank']
                    user_name.exam_score = request.POST['net_score']
                if(user_name.gate_status=='Other External Fellowships'):
                    user_name.detail_scholar=request.POST['detail_scholar']
                #user_name.score_card = request.FILES['score_card']
                user_name.degree = request.POST['degree']
                user_name.degree_status = request.POST['degree_status']
                user_name.degree_name = request.POST['dname']
                user_name.degree_uni = request.POST['uname']
                user_name.degree_disc = request.POST['ddisc']
                user_name.degree_year = request.POST['dyear']
                user_name.degree_score = request.POST['dscore']
                user_name.inter = request.POST['inter']
                user_name.inter_board = request.POST['inter_board']
                user_name.inter_subject = request.POST['inter_subject']
                user_name.inter_year = request.POST['inter_year']
                user_name.inter_score = request.POST['inter_score']
                user_name.high = request.POST['high']
                user_name.high_board = request.POST['high_board']
                user_name.high_subject = request.POST['high_subject']
                user_name.high_year = request.POST['high_year']
                user_name.high_score = request.POST['high_score']
                user_name.work_exp = request.POST['work_exp']
                user_name.period_from = request.POST['period_from']
                user_name.period_to = request.POST['period_to']
                user_name.work_org = request.POST['work_org']
                user_name.position = request.POST['position']
                user_name.registered = "Y"
                user_name.save()
                generate_pdf2(request)
                return HttpResponse("FormSubmitted")
        else:
            user_name = UserDetails2.objects.get(user=request.user)
            image_form = ImageForm()
            #if user_name.registered == "Y":
             #    return HttpResponse('You have submitted this part of the form Go to <a href="/register/part_form/">Next Part</a>')
            return render(request,'registration2.html',{'user_data':user_name,'image_form':image_form})
    else:
        print "from some"
        return HttpResponseRedirect('/register/login/')

@login_required(login_url='/register/login')

def view_formphd(request):
    user_name = UserDetails1.objects.get(user=request.user)
    lol1 = '1'+user_name.full_name+'.jpg'
    lol2 = '2'+user_name.full_name+'.jpg'
    lol3 = '3'+user_name.full_name+'.jpg'
    pdfs = request.user.username + '.pdf'
    return render(request,'view1.html',{'user_data':user_name,'lol1':lol1,'lol2':lol2,'lol3':lol3,'pdfs':pdfs})

def view_formpg(request):
    user_name = UserDetails2.objects.get(user=request.user)
    lol1 = request.user.username+'.jpg'
    lol2 = request.user.username+'.jpg'
    lol3 = request.user.username+'.jpg'
    pdfs = request.user.username + '.pdf'
    return render(request,'view2.html',{'user_data':user_name,'lol1':lol1,'lol2':lol2,'lol3':lol3,'pdfs':pdfs})

def generate_pdf(request):
    user = request.user
    user_data = UserDetails1.objects.get(user=user)
    data = {}
    data['application_id']=user_data.application_id
    data['full_name'] = user_data.full_name
    data['mother_name'] = user_data.mother_name
    data['father_name'] = user_data.father_name
    data['dob'] = user_data.dob
    data['dop'] = user_data.dop
    data['gender'] = user_data.gender
    data['nation'] = user_data.nation
    data['category'] = user_data.category
    data['gatestatus'] = user_data.gatestatus
    data['publica_status'] = user_data.publica_status
    data['gate_exam'] = user_data.gate_exam
    data['email'] = user_data.email
    data['phys'] = user_data.phys
    data['perma_addr'] = user_data.perma_addr
    data['corres_addr'] = user_data.corres_addr
    data['mobile'] = user_data.mobile
    data['ereceipt'] = user_data.ereceipt
    data['user'] = request.user.username
    data['gate_disc'] = user_data.gate_disc
    data['gate_roll'] = user_data.gate_roll
    data['gate_rank'] = user_data.gate_rank
    data['quali_degree'] = user_data.quali_degree
    data['univ_name'] = user_data.univ_name
    data['year_passing'] = user_data.year_passing
    data['status_deg'] = user_data.status_deg
    data['aggre_per'] = user_data.aggre_per
    #data['stu_status'] = user_data.stu_status
    #data['fin_status'] = user_data.fin_status
    data['disc_choice1'] = user_data.disc_choice1
    data['disc_choice2'] = user_data.disc_choice2
    data['disc_choice3'] = user_data.disc_choice3
    #data['disc_choice4'] = user_data.disc_choice4
    #data['disc_choice5'] = user_data.disc_choice5
    data['spec_choice1'] = user_data.spec_choice1
    data['spec_choice2' ] = user_data.spec_choice2
    data['spec_choice3'] = user_data.spec_choice3
    data['work_exp']  = user_data.work_exp
    data['period_from'] = user_data.period_from
    data['period_to'] = user_data.period_to
    data['work_org'] = user_data.work_org
    data['position'] = user_data.position
    data['publica'] = user_data.publica
    data['refree1_name'] = user_data.refree1_name
    data['refree2_name'] = user_data.refree2_name
    data['refree1_email'] = user_data.refree1_email
    data['refree2_email'] = user_data.refree2_email
    data['saved2'] = user_data.saved2
    temp = StringIO()
    p = canvas.Canvas(os.path.dirname(os.path.dirname(__file__))+'/static/pdfs/'+user.username+'.pdf')
    p = pdf.pdf_gen(p,data,user_data.full_name)
    return

def generate_pdf2(request):
    user = request.user
    user_data = UserDetails1.objects.get(user=user)
    data = {}
    data['application_id']=user_data.application_id
    data['full_name'] = user_data.full_name
    data['mother_name'] = user_data.mother_name
    data['father_name'] = user_data.father_name
    data['dob'] = user_data.dob
    data['dop'] = user_data.dop
    data['gender'] = user_data.gender
    data['nation'] = user_data.nation
    data['category'] = user_data.category
    data['gatestatus'] = user_data.gatestatus
    data['publica_status'] = user_data.publica_status
    data['gate_exam'] = user_data.gate_exam
    data['email'] = user_data.email
    data['phys'] = user_data.phys
    data['perma_addr'] = user_data.perma_addr
    data['corres_addr'] = user_data.corres_addr
    data['mobile'] = user_data.mobile
    data['ereceipt'] = user_data.ereceipt
    data['user'] = request.user.username
    data['gate_disc'] = user_data.gate_disc
    data['gate_roll'] = user_data.gate_roll
    data['gate_rank'] = user_data.gate_rank
    data['quali_degree'] = user_data.quali_degree
    data['univ_name'] = user_data.univ_name
    data['year_passing'] = user_data.year_passing
    data['status_deg'] = user_data.status_deg
    data['aggre_per'] = user_data.aggre_per
    #data['stu_status'] = user_data.stu_status
    #data['fin_status'] = user_data.fin_status
    data['disc_choice1'] = user_data.disc_choice1
    data['disc_choice2'] = user_data.disc_choice2
    data['disc_choice3'] = user_data.disc_choice3
    #data['disc_choice4'] = user_data.disc_choice4
    #data['disc_choice5'] = user_data.disc_choice5
    data['spec_choice1'] = user_data.spec_choice1
    data['spec_choice2' ] = user_data.spec_choice2
    data['spec_choice3'] = user_data.spec_choice3
    data['work_exp']  = user_data.work_exp
    data['period_from'] = user_data.period_from
    data['period_to'] = user_data.period_to
    data['work_org'] = user_data.work_org
    data['position'] = user_data.position
    data['publica'] = user_data.publica
    data['refree1_name'] = user_data.refree1_name
    data['refree2_name'] = user_data.refree2_name
    data['refree1_email'] = user_data.refree1_email
    data['refree2_email'] = user_data.refree2_email
    data['saved2'] = user_data.saved2
    temp = StringIO()
    p = canvas.Canvas(os.path.dirname(os.path.dirname(__file__))+'/static/pdfs/'+user.username+'.pdf')
    p = pdf.pdf_gen2(p,data,user_data.full_name)
    return

def logout(request):
    lgout(request)
    return render(request,'register/login.html',{'message':'You are logged out Successfully ....Enter below to login again'})
