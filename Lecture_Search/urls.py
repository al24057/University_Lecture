from django.urls import path
from . import views
app_name="Lecture_Search"

urlpatterns = [
    path("", views.index, name="index")
]