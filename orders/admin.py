from django.contrib import admin

from .models import Size, Pizza, Topping, Pasta, Salad, Dinner
# Register your models here.
admin.site.register(Size)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner)
