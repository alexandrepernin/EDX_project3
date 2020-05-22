from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return "{}".format(self.name)

class SubExtra(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return "{}".format(self.name)

class Pizza(models.Model):
    type = models.CharField(max_length=8, choices=[('regular', 'Regular'), ('sicilian', 'Sicilian')], default='regular')
    name = models.CharField(max_length=7, choices=[('cheese', 'Cheese'), ('special', 'Special')], default='cheese')
    toppings_nb = models.IntegerField(default=0, choices=[(0,'No Topping'), (1,'1 Topping'), (2, '2 Topping'), (3,'3 Topping')])
    toppings = models.ManyToManyField(Topping, blank=True, related_name="pizzas")
    size = models.CharField(max_length=1,choices=[('S', 'Small'), ('L', 'Large')], default='S')
    price_small = models.FloatField(default=0)
    price_large = models.FloatField(default=0)
    menu = models.BooleanField(default=False)

    def __str__(self):
        if self.menu==True:
            return f"{self.type.capitalize()}, {self.name.capitalize()}, {self.toppings_nb} top. (S: ${self.price_small} / L: ${self.price_large})"
        else:
            topping_string=list(set([topping.name for topping in self.toppings.all()]))
            topping_string='/'.join(topping_string)
            if self.size=='S':
                return f"Small {self.type.capitalize()} Pizza, {self.name.capitalize()}, {self.toppings_nb} toppings {topping_string} (${self.price_small})"
            else:
                return f"Large {self.type.capitalize()} Pizza, {self.name.capitalize()}, {self.toppings_nb} toppings {topping_string} (${self.price_large})"

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    menu = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({}$)".format(self.name, self.price)

class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    menu = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({}$)".format(self.name, self.price)

class Dinner(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=1,choices=[('S', 'Small'), ('L', 'Large')], default='S')
    price_small = models.FloatField(default=0)
    price_large = models.FloatField(default=0)
    menu = models.BooleanField(default=False)

    def __str__(self):
        if self.menu==True:
            return f"{self.name} (S: ${self.price_small} / L: ${self.price_large})"
        else:
            if self.size=="S":
                return f"Small Dinner, {self.name} ($ {self.price_small})"
            else:
                return f"Large Dinner, {self.name} ($ {self.price_large})"


class Sub(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=1,choices=[('S', 'Small'), ('L', 'Large')], default='S')
    price_small = models.FloatField(default=0)
    price_large = models.FloatField(default=0)
    menu = models.BooleanField(default=False)
    extra_cheese = models.BooleanField(default=False)
    extras = models.ManyToManyField(SubExtra, blank=True, related_name="subs")

    def __str__(self):
        if self.menu==True:
            return f"{self.name} (S: ${self.price_small} / L: ${self.price_large})"
        else:
            if self.size=="S":
                return f"Small Sub, {self.name} ($ {self.price_small})"
            else:
                return f"Large Sub, {self.name} ($ {self.price_large})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza, blank=True, related_name="orders")
    salads = models.ManyToManyField(Salad, blank=True, related_name="orders")
    pastas = models.ManyToManyField(Pasta, blank=True, related_name="orders")
    dinners = models.ManyToManyField(Dinner, blank=True, related_name="orders")
    subs = models.ManyToManyField(Sub, blank=True, related_name="orders")
    created = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False)
    total = models.FloatField(default=0)

    def compute_total(self):
        self.total=0
        for pizza in self.pizzas.all():
            self.total+=pizza.price_small if pizza.size=='S' else pizza.price_large
        for salad in self.salads.all():
            self.total+=salad.price
        for pasta in self.pastas.all():
            self.total+=pasta.price
        for dinner in self.dinners.all():
            self.total+=dinner.price_small if dinner.size=='S' else dinner.price_large
        for sub in self.subs.all():
            price=sub.price_small if sub.size=='S' else sub.price_large
            if sub.extra_cheese:
                price+=0.50
            for extra in sub.extras.all():
                price+=0.50
            self.total+=price
        self.total = round(self.total, 2)
        self.save()
        return False

    def __str__(self):
        date=self.created.strftime("%H:%M (%d-%b-%Y)")
        return f"Order ID#{self.id}: [{date}] for {self.user.username}"
