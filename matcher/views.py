from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .utils import extract_resume_text


def home(request):
    score = None

    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        job_desc = request.POST.get('job_desc')

        if resume_file and job_desc:
            resume_text = extract_resume_text(resume_file)

            # temporary matching logic
            if job_desc.lower() in resume_text.lower():
                score = 90
            else:
                score = 50

    return render(request, 'home.html', {'score': score})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')