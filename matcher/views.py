from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# ================= HOME PAGE =================

@login_required(login_url='login')
def home(request):

    context = {
        'score': 0,
        'matched_skills': [],
        'missing_skills': [],
        'recommendation': '',
        'strength': '',
        'recommended_roles': [],
        'job_role': '',
        'company': '',
        'job_desc': '',
        'required_skills': '',
        'user_skills': '',
    }

    if request.method == 'POST':

        # USER INPUTS
        user_skills = request.POST.get('skills', '')
        job_role = request.POST.get('job_role', '')
        company = request.POST.get('company', '')
        job_desc = request.POST.get('job_desc', '')
        required_skills = request.POST.get('required_skills', '')

        # CONVERT TO LIST
        user_skill_list = [
            skill.strip().lower()
            for skill in user_skills.split(',')
            if skill.strip()
        ]

        required_skill_list = [
            skill.strip().lower()
            for skill in required_skills.split(',')
            if skill.strip()
        ]

        # MATCHED SKILLS
        matched_skills = list(
            set(user_skill_list) & set(required_skill_list)
        )

        # MISSING SKILLS
        missing_skills = list(
            set(required_skill_list) - set(user_skill_list)
        )

        # SCORE
        if len(required_skill_list) > 0:

            score = int(
                (len(matched_skills) / len(required_skill_list)) * 100
            )

        else:
            score = 0

        # RECOMMENDATION
        if score >= 80:
            recommendation = "Selected"
            strength = "Strong Candidate"

        elif score >= 50:
            recommendation = "Moderate Match"
            strength = "Intermediate Candidate"

        else:
            recommendation = "Rejected"
            strength = "Beginner Candidate"

        # CAREER ROLE SUGGESTION
        recommended_roles = []

        if 'python' in user_skill_list:
            recommended_roles.append('Python Developer')

        if 'django' in user_skill_list:
            recommended_roles.append('Django Developer')

        if 'html' in user_skill_list:
            recommended_roles.append('Frontend Developer')

        if 'javascript' in user_skill_list:
            recommended_roles.append('JavaScript Developer')

        if 'react' in user_skill_list:
            recommended_roles.append('React Developer')

        # CONTEXT
        context = {
            'score': score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'recommendation': recommendation,
            'strength': strength,
            'recommended_roles': recommended_roles,
            'job_role': job_role,
            'company': company,
            'job_desc': job_desc,
            'required_skills': required_skills,
            'user_skills': user_skills,
        }

    return render(request, 'home.html', context)


# ================= SIGNUP =================

def signup_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists'
            )

            return redirect('signup')

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(
            request,
            'Account Created Successfully'
        )

        return redirect('login')

    return render(request, 'signup.html')


# ================= LOGIN =================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(
                request,
                'Invalid Username or Password'
            )

    return render(request, 'login.html')


# ================= LOGOUT =================

def logout_view(request):

    logout(request)

    return redirect('login')