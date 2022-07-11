import email
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Myuser

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            new_user = Myuser(user_name = username,email_id = email)
            new_user.save()
            messages.success(request,f'Account Created For {username}!')
            return redirect('login')   

    form = UserRegistrationForm()
    context = {
        'form' : form
    }
    return render(request,'login/register.html',context)

def login(request):
    context = {
        'Hello' : "Login page"
    }
    return render(request,'login/login.html',context)


