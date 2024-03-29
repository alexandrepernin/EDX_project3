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
        "SubExtras": SubExtra.objects.all(),
        "Salads": Salad.objects.filter(menu=True),
        "Pastas": Pasta.objects.filter(menu=True),
        "Dinners": Dinner.objects.filter(menu=True),
        "Subs": Sub.objects.filter(menu=True),
        "Orders": Order.objects.filter(validated=False, user=request.user)
    }
    logger.error("Processing code for index")
    return render(request, "orders/index.html", context)

def ask_confirmation(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "Orders": Order.objects.filter(validated=False, user=request.user)
    }
    return render(request, "orders/confirm.html", context)

def confirm(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    order = Order.objects.filter(validated=False, user=request.user)
    if order:
        order = order[0]
    order.validated=True
    order.save()
    message="Thanks for shopping with us!"
    return render(request, "orders/thanks.html", {"message":message})

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
    order = Order.objects.filter(validated=False, user=request.user)
    if order:
        order=order[0]
    else:
        order=Order(validated=False, user=request.user)
        order.save()
    order.salads.add(salad)
    order.save()
    order.compute_total()
    return JsonResponse({"success": True})

@csrf_exempt
def order_pasta(request):
    data = request.POST["pasta_type"]
    username=request.user.username
    logger.error("Processing code for order_pasta: {} for user {}".format(data, username))
    pasta_menu = Pasta.objects.filter(name=data, menu=True)[0]
    pasta = Pasta(menu=False, price=pasta_menu.price, name=pasta_menu.name)
    pasta.save()
    order = Order.objects.filter(validated=False, user=request.user)
    if order:
        order=order[0]
    else:
        order=Order(validated=False, user=request.user)
        order.save()
    order.pastas.add(pasta)
    order.save()
    order.compute_total()
    return JsonResponse({"success": True})

@csrf_exempt
def order_dinner(request):
    dinner_name = request.POST["dinner"]
    dinner_size = request.POST["size"][:1]
    username=request.user.username
    logger.error("Processing code for order_dinner: {} of size {} for user {}".format(dinner_name, dinner_size, username))
    dinner_menu = Dinner.objects.filter(name=dinner_name, menu=True)[0]
    dinner_to_add = Dinner(menu=False, name=dinner_name, size=dinner_size, price_small=dinner_menu.price_small, price_large=dinner_menu.price_large)
    dinner_to_add.save()
    order = Order.objects.filter(validated=False, user=request.user)
    if order:
        order=order[0]
    else:
        order=Order(validated=False, user=request.user)
        order.save()
    order.dinners.add(dinner_to_add)
    order.save()
    order.compute_total()
    return JsonResponse({"success": True})

@csrf_exempt
def order_sub(request):
    sub_name = request.POST["sub"]
    sub_size = request.POST["size"][:1]
    extras = dict()
    for extra in ["Cheese", "Onions", "Mushrooms", "Green Peppers"]:
        extras[extra] = request.POST[extra]=='true'
    username=request.user.username
    logger.error("Processing code for order_sub: {} of size {} for user {}".format(sub_name, sub_size, username))
    order = Order.objects.filter(validated=False, user=request.user)
    if order:
        order=order[0]
    else:
        order=Order(validated=False, user=request.user)
        order.save()
    sub_menu = Sub.objects.filter(menu=True, name=sub_name)[0]
    sub_to_add = Sub(menu=False, name=sub_name, size=sub_size, price_small=sub_menu.price_small,
                    price_large=sub_menu.price_large, extra_cheese=extras["Cheese"])
    sub_to_add.save()
    for extra in ["Onions", "Mushrooms", "Green Peppers"]:
        if extras[extra]:
            sub_to_add.extras.add(SubExtra.objects.filter(name=extra)[0])
    sub_to_add.save()
    order.subs.add(sub_to_add)
    order.save()
    order.compute_total()
    logger.error("Adding to order the sub"+str(sub_to_add))
    return JsonResponse({"success": True})

@csrf_exempt
def order_pizza(request):
    logger.error("Processing code for order_pizza")
    username=request.user.username
    #Dealing with name and type
    pizza = request.POST["pizza"].split(',')
    pizza = [info.strip() for info in pizza]
    type = pizza[0]
    type = type[0].lower() + type[1:]
    name = pizza[1]
    name = name[0].lower()+ name[1:]
    #Dealing with toppings
    ordered_toppings = []
    topping_list = Topping.objects.all()
    topping_list = [x.name for x in topping_list]
    for id in [1,2,3]:
        from_form = request.POST[f"top{id}"]
        if from_form in topping_list:
            ordered_toppings.append(from_form)
    ordered_toppings = list(set(ordered_toppings))
    ## Should not be executed. #TODO=> disable topping submission for specials:
    if name=="special":
        ordered_toppings = []
    topping_nb = len(ordered_toppings)
    #Dealing with size
    size = request.POST["size"]
    size=size[:1]
    logger.error(f"{username}: {type} pizza {name} of size {size} with {topping_nb} toppings")
    #Prices
    pizza_menu = Pizza.objects.filter(menu=True, type=type, name=name, toppings_nb=topping_nb)[0]
    price_small = pizza_menu.price_small
    price_large = pizza_menu.price_large
    #Adding toppings to pizza
    pizza_to_add = Pizza(menu=False, type=type, name=name, size=size, price_small=price_small, price_large=price_large, toppings_nb=topping_nb)
    pizza_to_add.save()
    for topping in ordered_toppings:
        topping_to_add = Topping.objects.filter(name=topping)[0]
        pizza_to_add.toppings.add(topping_to_add)
    pizza_to_add.save()
    #Adding pizza to order
    logger.error("Adding to order the pizza"+str(pizza_to_add))
    order = Order.objects.filter(user=request.user, validated=False)
    if order:
        order=order[0]
    else:
        order=Order(validated=False, user=request.user)
        order.save()
    order.pizzas.add(pizza_to_add)
    order.save()
    order.compute_total()
    return JsonResponse({"success": True})
