from django.contrib import admin

from .models import Pizza, Topping, SubExtra, Pasta, Salad, Dinner, Sub, Order

class PizzaAdmin(admin.ModelAdmin):
      filter_horizontal = ("toppings",)
      list_filter = ('menu',)

class SaladAdmin(admin.ModelAdmin):
    list_filter = ('menu',)

class PastaAdmin(admin.ModelAdmin):
    list_filter = ('menu',)

class DinnerAdmin(admin.ModelAdmin):
    list_filter = ('menu',)

class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ("pizzas","salads", "pastas", "dinners")
    list_filter = ('validated',)

# Register your models here.
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Topping)
admin.site.register(SubExtra)
admin.site.register(Pasta, PastaAdmin)
admin.site.register(Salad, SaladAdmin)
admin.site.register(Dinner, DinnerAdmin)
admin.site.register(Sub)
admin.site.register(Order, OrderAdmin)
