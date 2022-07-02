from multiprocessing import context
from django.shortcuts import render

def login(request):
    context = {
        'Hello' : "Login page"
    }
    return render(request,'login/login.html',context)

