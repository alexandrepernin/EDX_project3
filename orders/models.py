from django.db import models

# Create your models here.
class Size(models.Model):
    name=models.CharField(max_length=64)

    def __str__(self):
        return "Size: {}".format(self.name)

class Pizza(models.Model):
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    toppings = models.IntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def __str__(self):
        return "Pizza {}, {} with {} toppings of size {}".format(self.type, self.name, self.toppings, self.size)

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return "Topping #{}: {}".format(self.id, self.name)

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return "Pasta #{}: {}".format(self.id, self.name)

class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return "Salad #{}: {}".format(self.id, self.name)

class Dinner(models.Model):
    name = models.CharField(max_length=64)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return "Dinner Platter #{}: {}. {}.".format(self.id, self.name, self.size)
