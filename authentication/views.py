import math
import random
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_decode_handler
from authentication.serializer import *
import json
import smtplib
from glob import escape
from django.utils.translation import gettext as _
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from authentication.models import *
# Create your views here.   

def jwt_payload_handler(user):
    return {
        "id" :user.pk,
        "email":user.email,
        "name":user.name,
    }
def verifyToken(token):
    try:
        decode = jwt_decode_handler(token)
        return decode
    except:
        return {"result" : False }

def getOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def sendMail(email,OTP): 
    password = "kvznxpcmozscvcaj"
    
    msg = MIMEMultipart()
    msg['From'] = "akashs@krishworks.com"
    msg['To'] = email
    msg['Subject'] = "Auth App OTP Verification"
    body = "Hey {} ..!".format(escape("akash")) + "\n"
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("akashsachanboss@gmail.com", password)
    body += "Auth App OTP is : {}".format(OTP)
        
    print("mail", body)
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    s.sendmail("akashsachanboss@gmail.com", email, text)
    print("mail succesfully")
    s.quit()

class Login(APIView):
     def post(self,request):
            data =  request.data
            email = data["email"]
            password = data["password"]
            errors = {}
            if not email:
                errors['email'] = ['This field is required']
            if not password:
                errors['password'] = ['This field is required']
            if errors:
                return Response({'error': True, 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=email).first()
            if not user:
                return Response(
                    {"error": True, "errors": "user not avaliable in our records"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user.check_password(password):
                response_data = {}
                payload = jwt_payload_handler(user)
                if(user.is_verified) :
                    response_data = {
                        "token" : jwt_encode_handler(payload),
                    "error": False
                    }
            
                else:
                    response_data["error"] = True
                    response_data["message"] = "Account is not Verified Yet"
                return Response(response_data, status=status.HTTP_200_OK)
            password_field = "doesnot match"
            msg = _("Email and password {password_field}")
            msg = msg.format(password_field=password_field)
            return Response(
                {"error": True, "errors": msg},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Signup(APIView):
    def post(self,request):
        data = request.data
        print("akash",data)
        check  = User.objects.filter(email = data["email"])
        OTP = getOTP()
        print(check)
        if check.exists():
            check = check[0]
            if  check.is_verified:
                return Response(
                    {"error": False, "message": "User already exists."},
                    status=status.HTTP_208_ALREADY_REPORTED,
                )
            else:
                sendMail(data['email'],OTP=OTP)
                check.otp_email = OTP
                check.save()
                return Response(
                    {"error": True, "message": "User created SuccessFully."},
                    status=status.HTTP_200_OK,
                )
        form = SignUpSerializer(data=data)
        """
        {
        "name":"Akash",
        "email":"akashs@krishworks.com",
        "phone_number":"+917007796127",
        "password":"pass2023"
        }
        
        """
        if form.is_valid():
            name = data['name']
            email = data['email']
            password = data['password']
            user = User(email = email,name=name,phone_number = data['phone_number'],otp_email = OTP)
            user.set_password(password)
            user.save()
            sendMail(email=email,OTP=OTP)
            return Response(
                    {"error": False, "message": "User created Successfully."},
                    status=status.HTTP_200_OK,
                )
        return Response({'error': True, 'errors': form.errors},
                        status=status.HTTP_400_BAD_REQUEST)

class VerifySignUp(APIView):
        # def get(self,request):
        #     data = request.data
    """
        {
        "email":"akashs@krishworks.com",
        "otp":"771764"
        }
        
        """

    def post(self,request):
        data = request.data
        check = User.objects.filter(email = data["email"])
        if check.exists():
            check = check[0]
            # print("otp",type(check.otp_email),type(data['otp']),check.otp_email == data['otp'])
            if check.otp_email == data['otp']:
                check.is_verified = True
                check.save()
                return Response(
                    {
                        "error":False,
                        "message":"Email is verified"
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": True, "message": "Incorrect OTP"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        

class LoginView(APIView):
        """
        {
        "name":"Akash",
        "email":"akashs@krishworks.com",
        "phone_number":"+917007796127",
        "password":"pass2023"
        }
        
        """
        def post(self,request):
            data =  request.data
            email = data["email"]
            password = data["password"]
            errors = {}
            if not email:
                errors['email'] = ['This field is required']
            if not password:
                errors['password'] = ['This field is required']
            if errors:
                return Response({'error': True, 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=email).first()
            if not user:
                return Response(
                    {"error": True, "errors": "user not avaliable in our records"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user.check_password(password):
                payload = jwt_payload_handler(user)
                response_data = {
                    "token": jwt_encode_handler(payload),
                    "error": False,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            password_field = "doesnot match"
            msg = _("Email and password {password_field}")
            msg = msg.format(password_field=password_field)
            return Response(
                {"error": True, "errors": msg},
                status=status.HTTP_400_BAD_REQUEST,
            )
