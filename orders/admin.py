from django.contrib import admin

from .models import Pizza, Topping, Pasta, Salad, Dinner, Sub, Order

class PizzaAdmin(admin.ModelAdmin):
      filter_horizontal = ("toppings",)

# Register your models here.
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Topping)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner)
admin.site.register(Sub)
admin.site.register(Order)
