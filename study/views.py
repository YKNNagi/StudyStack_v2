from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Study
from .forms import StudyForm
from .forms import SignupForm

def index(request):
    return HttpResponse("StudyStack")

def signup(request):
    if request.method == "POST":

        #登録ボタンを押した
        form =SignupForm(request.POST)

        if form.is_valid():
            form.save()
        
    else:

        #最初に登録画面を開いたとき
        form = SignupForm()

    return render(request, "study/signup.html", {"form": form})



def login_view(request):
    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("dashboard")
      
    else:
        form = AuthenticationForm()

    return render(request, "study/login.html", {"form": form})

@login_required(login_url="/login/")
def dashboard(request):

    studies = Study.objects.filter(
        user=request.user
    ).order_by("-created_at")

    if request.method == "POST":
        form = StudyForm(request.POST)

        if form.is_valid():
            study = form.save(commit=False)
            study.user = request.user
            study.save()
            form.save_m2m()

            return redirect("dashboard")

    else:
        form = StudyForm()

    context = {
        "studies" : studies,
        "form" : form
    }

    return render(request, "study/dashboard.html", context)


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)

    return redirect("login")


@login_required(login_url="/login/")
def update_view(request,study_id):

    study = get_object_or_404(
        Study,
        id=study_id,
        user=request.user
    )

    if request.method == "POST":
        form = StudyForm(request.POST, instance=study)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
            form = StudyForm(instance = study)

    return render(
        request,
        "study/update.html",
        {"form": form}
    )

@login_required(login_url="/login/")
def delete_view(request, study_id):

    study = get_object_or_404(
        Study,
        id=study_id,
        user=request.user
    )

    if request.method == "POST":
        study.delete()

    return redirect("dashboard")