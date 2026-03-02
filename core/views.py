from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Job
from .models import Job, Internship 

# Temporary in-memory storage (demo purpose only)
uploaded_resumes = {}
cover_letters = {}
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Check if this user is superuser (admin)
            if user.is_superuser:
                return redirect("/admin/")   # redirect to admin panel
            else:
                return redirect("/")         # redirect to home page
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    
    return render(request, "login.html")

# ------------------ Home & Bot ------------------
def home(request):
    return render(request, 'core/home.html')

def jobbot(request):
    return render(request, 'core/jobbot.html')

# ------------------ Auth System ------------------
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # username exists?
        if User.objects.filter(username=username).exists():
            return render(request, "core/auth.html", {"error": "⚠️ Username already taken."})

        # email exists?
        if User.objects.filter(email=email).exists():
            return render(request, "core/auth.html", {"error": "⚠️ Email already registered."})

        # password check
        if password1 != password2:
            return render(request, "core/auth.html", {"error": "⚠️ Passwords do not match."})

        # create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)  # auto login after signup
        return redirect("home")

    return render(request, "core/auth.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "⚠️ Invalid username or password")
            return render(request, "core/auth.html")

    return render(request, "core/auth.html")


def logout_view(request):
    logout(request)
    return redirect("login")

# ------------------ Job Flow ------------------
def upload_resume(request):
    tips = "💡 Make sure your resume highlights key skills and projects."
    uploaded_file_url = None

    if request.method == 'POST' and request.FILES.get('resume_file'):
        resume_file = request.FILES['resume_file']
        fs = FileSystemStorage()
        filename = fs.save(resume_file.name, resume_file)
        uploaded_file_url = fs.url(filename)

        uploaded_resumes[request.session.session_key] = {
            'filename': filename,
            'url': uploaded_file_url
        }
        return redirect('jobs_match')

    return render(request, 'core/jobs_upload.html', {
        'uploaded_file_url': uploaded_file_url,
        'tips': tips
    })


def jobs_match(request):
    uploaded_resume_skills = ["python", "django", "html", "css", "sql"]

    all_jobs = Job.objects.all()
    matching_jobs = []

    for job in all_jobs:
        job_skills = [skill.strip().lower() for skill in job.required_skills.split(",")]
        matched = [s for s in uploaded_resume_skills if s in job_skills]

        if matched:
            match_percent = int((len(matched) / len(job_skills)) * 100)
            job.match_percent = match_percent
            job.matched_skills = matched
            matching_jobs.append(job)

    growth_tip = "Learn React.js to improve frontend opportunities 🚀"

    context = {
        "matching_jobs": matching_jobs,
        "growth_tip": growth_tip,
        "skills": uploaded_resume_skills,
        "missing_skills": ["react", "docker"],
        "tips": "Keep updating your resume regularly!"
    }
    return render(request, "core/jobs_match.html", context)


def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    resume_data = uploaded_resumes.get(request.session.session_key)

    if request.method == 'POST':
        return redirect('cover_letter', job_title=job.title)

    return render(request, 'core/jobs_apply.html', {'job': job, 'resume': resume_data})


def cover_letter(request, job_title):
    if request.method == 'POST':
        cover_letter_text = request.POST.get('cover_letter')
        cover_letters[request.session.session_key] = cover_letter_text
        return redirect('application_success')
    return render(request, 'core/cover_letter.html', {'job_title': job_title})


def application_success(request):
    return render(request, 'core/success.html')

# ------------------ Internship Flow ------------------
# 1️⃣ Resume Upload
def intern_upload(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        resume = request.FILES['resume']
        fs = FileSystemStorage()
        filename = fs.save(resume.name, resume)
        uploaded_file_url = fs.url(filename)
        request.session['resume_url'] = uploaded_file_url
        return redirect('intern_match')
    return render(request, 'core/interns_upload.html')  # ✅ Template name fix

# 2️⃣ Show Match % for all internships
# 2️⃣ Show Match % for all internships
from django.shortcuts import render, redirect
from .models import Internship

def intern_match(request):
    if not request.session.get('resume_url'):
        return redirect('intern_upload')

    internships = Internship.objects.all()
    results = []

    uploaded_resume_skills = ["python", "django", "html", "css"]  # Example skills

    for intern in internships:
        required = [s.strip().lower() for s in intern.skills.split(",")] if intern.skills else []
        matched = [s for s in uploaded_resume_skills if s in required]

        match_percent = int((len(matched) / len(required)) * 100) if required else 0

        results.append({
            "id": intern.id,
            "title": intern.title,
            "company": intern.company,
            "location": intern.location,
            "stipend": intern.stipend,
            "duration": intern.duration,
            "match": match_percent,
            "skills": required,        # full list (admin input)
            "matched_skills": matched  # only matched skills
        })

    request.session['internships'] = results
    return render(request, 'core/interns_match.html', {"internships": results})
  # ✅ Template name fix

# 3️⃣ Apply for specific internship → Cover Letter
def intern_apply(request, intern_id):
    internship = get_object_or_404(Internship, id=intern_id)

    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')
        request.session['cover_letter'] = cover_letter
        return redirect('intern_success')

    context = {
        'internship': internship
    }
    return render(request, 'core/intern_cover.html', context)  # ✅ Template name fix

# 4️⃣ Success page
def intern_success(request):
    return render(request, 'core/success.html')