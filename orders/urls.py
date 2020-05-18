from django.urls import path

from . import views

#urlpatterns: list of the routes. views contains the method to route for the associated route
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("signup", views.signup_view, name="signup"),
    path("logout", views.logout_view, name="logout"),
    path("order_salad", views.order_salad, name="order_salad"),
    path("order_pasta", views.order_pasta, name="order_pasta")
]
