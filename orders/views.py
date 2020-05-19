from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import logging

from .models import *

logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user,
        "Pizzas": Pizza.objects.filter(menu=True),
        "Toppings": Topping.objects.all(),
        "Salads": Salad.objects.filter(menu=True),
        "Pastas": Pasta.objects.filter(menu=True),
        "Orders": Order.objects.filter(validated=False, user=request.user)
    }
    logger.error("Processing code for index")
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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            render(request, "orders/signup.html", {"message": "A problem has occurred."})

def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})

@csrf_exempt
def order_salad(request):
    data = request.POST["salad_type"]
    username=request.user.username
    logger.error("Processing code for order_salad: {} for user {}".format(data, username))
    salad_menu = Salad.objects.filter(name=data, menu=True)[0]
    salad = Salad(menu=False, price=salad_menu.price, name=salad_menu.name)
    salad.save()
    order = Order.objects.filter(validated=False, user=request.user)[0]
    order.salads.add(salad)
    order.save()
    return JsonResponse({"success": True})

@csrf_exempt
def order_pasta(request):
    data = request.POST["pasta_type"]
    username=request.user.username
    logger.error("Processing code for order_pasta: {} for user {}".format(data, username))
    pasta_menu = Pasta.objects.filter(name=data, menu=True)[0]
    pasta = Pasta(menu=False, price=pasta_menu.price, name=pasta_menu.name)
    pasta.save()
    order = Order.objects.filter(validated=False, user=request.user)[0]
    order.pastas.add(pasta)
    order.save()
    return JsonResponse({"success": True})

@csrf_exempt
def order_pizza(request):
    logger.error("Processing code for order_pizza")
    username=request.user.username
    name = request.POST["name"]
    type = request.POST["type"]
    size = request.POST["size"]
    topping_nb = request.POST["toppings_nb"]
    #pizza_menu = Pizza.objects.filter(menu=True, type=type, name=name, size=size, toppings_nb=topping_nb)[0]
    logger.error("{}, {}, {} and {} for user {}".format(name, type, size, topping_nb, username))
    #logger.error(str(pizza_menu))
    return JsonResponse({"success": True})
