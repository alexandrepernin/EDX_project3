from django.db import models

# Create your models here.

class Pizza(models.Model):
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    toppings = models.IntegerField()
    size = models.CharField(max_length=64)

    def __str__(self):
        return "Pizza {}, {} with {} toppings of size {}".format(self.type, self.name, self.toppings, self.size)
