# Django Modules
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse

# Custom Modules Work as a tool
import random

# DataBase module import session
from base.models import OTPVerification

# Email Configuration modules
from django.core.mail import send_mail
from django.utils import timezone


def generate_otp():
    # Generate a 6-digit OTP (you can adjust the length as needed)
    return ''.join(random.choices('0123456789', k=6))

def enter_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return redirect('login')
        else:
            recipient_name = email.split('@')[0]
            recipient_email = email.replace('@gmail.com', '')

            otp_value = generate_otp()
            subject = '🔐 Login Verification for Your New Account'
            body = (
                '<html>'
                '<body style="font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">'
                '<h1 style="color: #333;">🔐 Login Verification for Your Account</h1>'
                '<p style="font-size: 16px; color: #666;">'
                f'Dear {recipient_name},<br><br>'
                'Please use the following OTP to verify your login: 🔑<br><br>'
                f'<strong>{otp_value}</strong><br><br>'
                'If you did not request this login verification, please ignore this email.<br><br>'
                'Thank you for using our services. 🙏<br><br>'
                'Best regards,<br>'
                'MyGuruPlus Team'
                '</p>'
                '</body>'
                '</html>'
            )
            print(otp_value)
            send_mail(
                subject,                         # subject
                body,      # body
                'sitejec@gmail.com',                        # sender Email
                [email],                                    # receiver mail
                html_message=body,
                fail_silently=False,
            )
            otp_verification = OTPVerification(email=email,otp_key=otp_value)
            otp_verification, created = OTPVerification.objects.get_or_create(
                email=email,
                defaults={'otp_key': otp_value}
            )
            # If the email already existed, update the OTP value
            if not created:
                otp_verification.otp_key = otp_value
                otp_verification.updated_time = timezone.now()
                otp_verification.save()
            obj = OTPVerification.objects.get(email=email)
            print("otp sent...", otp_value, "last updated value is : ", obj.otp_key)
            return redirect('signup', mail=email)
    return render(request,"auth/otp_verification.html")


def signup(request, mail):
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # Check if the username is already taken
            obj = OTPVerification.objects.get(email=mail)
            # check if the otp is match or not
            if otp == obj.otp_key:
                time_difference = timezone.now() - obj.updated_time
                if time_difference.total_seconds() <= 120:  # 120 seconds = 2 minutes
                    if User.objects.filter(username=username).exists():
                        return render(request, "auth/signup.html", {"mail":mail, "msg":"User name already exist. try any different name"})
                    else:
                        # Create the user
                        user = User.objects.create_user(username=username, email=mail, password=password)
                        login(request, user)
                        return redirect('home')  # Redirect to your home page
                else:
                    # The OTP was not updated within the last 2 minutes, handle accordingly
                    return render(request, "auth/signup.html", {"mail": mail, "msg": "The OTP has expired. Please enter a new one to create your password. <a href='/enter_otp'>Click here</a> to redirect."})

            else:
                return render(request, "auth/signup.html", {"mail":mail, "msg":"The Otp do not match, Try again"})
        else:
            return render(request, "auth/signup.html", {"mail":mail, "msg":"Passwords do not match"})
    
    return render(request, 'auth/signup.html',{"mail":mail})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('list_folders', path='root')
            else:
                return redirect('home')  # Redirect to your home page
        else:
            return redirect('login')
    
    return render(request, 'auth/login.html')
