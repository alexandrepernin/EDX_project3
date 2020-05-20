from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Topping(models.Model):
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
            if self.size=='S':
                return f"Small {self.type.capitalize()} Pizza, {self.name.capitalize()}, {self.toppings_nb} toppings (${self.price_small})"
            else:
                return f"Large {self.type.capitalize()} Pizza, {self.name.capitalize()}, {self.toppings_nb} toppings (${self.price_large})"

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
    price = models.FloatField()
    extra = models.BooleanField()
    menu = models.BooleanField(default=False)

    def __str__(self):
        return "Sub #{}: {}. {}.".format(self.id, self.name, self.size)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza, blank=True, related_name="orders")
    salads = models.ManyToManyField(Salad, blank=True, related_name="orders")
    pastas = models.ManyToManyField(Pasta, blank=True, related_name="orders")
    dinners = models.ManyToManyField(Dinner, blank=True, related_name="orders")
    created = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False)

    def __str__(self):
        date=self.created.strftime("%H:%M (%d-%b-%Y)")
        return f"Order ID#{self.id}: [{date}] for {self.user.username}"
