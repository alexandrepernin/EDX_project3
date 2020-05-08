from django.urls import path

from . import views

#urlpatterns: list of the routes. views contains the method to route for the associated route
urlpatterns = [
    path("", views.index, name="index")
]
