from django.views.generic import View
from bson.json_util import loads,dumps
from pymongo import MongoClient
from django.http import HttpResponse
import smtplib
from datetime import datetime
dbClient = MongoClient(host='localhost',port=27017)
db = dbClient['sample']

class Start(View):
    def get(self,request):
        result = {'message': '', 'code': 400, 'status': 'failed'}
        try:
            print('in hereeeeeeee')
            result = {'message': 'name is required'}
            if 'name' in request.GET and request.GET['name']!='':
                result = startDef(request.GET['name'],result)
        except Exception as e:
            result.update({'message':str(e)})
        return HttpResponse(dumps(result))
def startDef(name,result):
    try:
        userInfo = loads(dumps(db.users.find({'name':name},{'_id':0})))
        result.update({'message':'Invalid user'})
        if userInfo:
            result.update({'message':'welcome '+name,'status':'success','code':200})
    except Exception as e:
        result.update({'message': str(e)})
    return result

class EmailNotify(View):
    def get(self,request):
        result = {'message': '', 'code': 400, 'status': 'failed'}
        try:
            print('**************')
            result = {'message': 'email is required'}
            if 'email' in request.GET and request.GET['email'] != '':
                result = emailNotifyDef(request.GET['email'], result)
        except Exception as e:
            result.update({'message': str(e)})
        return HttpResponse(dumps(result))
def emailNotifyDef(email,result):
    try:
        # Create your SMTP session
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        # Use TLS to add security
        smtp.starttls()
        # User Authenticationw
        smtp.login("sasikiran.honey@gmail.com", "Honeysasi@123")
        # Defining The Message
        message = "This is test msg from python"
        # Sending the Email
        smtp.sendmail("sasikiran.honey@gmail.com", email, message)
        # Terminating the session
        smtp.quit()
        print("Email sent successfully!")
        result.update({'message':'please verify your '+email,'status':'success','code':200})
    except Exception as e:
        result.update({'message': str(e)})
    return result

def currentTime():
    print(datetime.now())
    
class ValidateUser(View):
    def get(self,request):
        result = {'message': '', 'code': 400, 'status': 'failed'}
        try:
            result = {'message': 'name is required'}
            if 'name' in request.GET and request.GET['name']!='':
                result = validateUserDef(request.GET['name'],result)
        except Exception as e:
            result.update({'message':str(e)})
        return HttpResponse(dumps(result))
def validateUserDef(name,result):
    try:
        userInfo = loads(dumps(db.users.find({'name':name},{'_id':0})))
        result.update({'message':'Invalid user'})
        if userInfo:
            result.update({'message':'hello '+name,'status':'success','code':200})
    except Exception as e:
        result.update({'message': str(e)})
    return result

def dec(func):
    name = 'sasi'
    return func(name)
@dec
def second(name):
    print('hello ',name)
