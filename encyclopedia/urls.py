from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("modify", views.modify, name="modify"),
    path("newpage", views.newpage, name="newpage"),
    path("randpage", views.randpage, name="randpage"),
    path("wiki/<str:wikititle>", views.wikipage, name="wikipage"),
]
