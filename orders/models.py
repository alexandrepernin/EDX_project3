from django.db import models

# Create your models here.
class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return "Topping #{}: {}".format(self.id, self.name)

class Pizza(models.Model):
    type = models.CharField(max_length=7, choices=[('regular', 'Regular'), ('sicilian', 'Sicilian')], default='regular')
    name = models.CharField(max_length=7, choices=[('cheese', 'Cheese'), ('special', 'Special')], default='cheese')
    toppings_nb = models.IntegerField(default=0, choices=[(0,'No Topping'), (1,'1 Topping'), (2, '2 Topping'), (3,'3 Topping')])
    toppings = models.ManyToManyField(Topping, blank=True, related_name="pizzas")
    size = models.CharField(max_length=1,choices=[('S', 'Small'), ('L', 'Large')], default='S')
    price = models.FloatField()

    def __str__(self):
        return "Pizza {}, {} with {} toppings of {} ({}$)".format(self.type, self.name, self.toppings_nb, self.size, self.price)

class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return "Pasta #{}: {} ({}$)".format(self.id, self.name, self.price)

class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return "Salad #{}: {} ({}$)".format(self.id, self.name, self.price)

class Dinner(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=1,choices=[('S', 'Small'), ('L', 'Large')], default='S')
    price = models.FloatField()

    def __str__(self):
        return "Dinner Platter #{}: {}. {} ({}$)".format(self.id, self.name, self.size, self.prize)

class Sub(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=1,choices=[('S', 'Small'), ('L', 'Large')], default='S')
    price = models.FloatField()
    extra = models.BooleanField()

    def __str__(self):
        return "Sub #{}: {}. {}.".format(self.id, self.name, self.size)
