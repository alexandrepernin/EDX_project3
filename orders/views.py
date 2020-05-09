from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import Pizza
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user,
        "Pizzas": Pizza.objects.all()
    }
    return render(request, "orders/index.html", context)

def login_view(request):
    if request.method=="GET":
        return render(request, "orders/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credentials."})

def signup_view(request):
    if request.method=="GET":
        return render(request, "orders/signup.html")
    else:
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})
