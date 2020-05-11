from django.contrib import admin

from .models import Pizza, Topping, Pasta, Salad, Dinner, Sub
# Register your models here.
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner)
admin.site.register(Sub)
