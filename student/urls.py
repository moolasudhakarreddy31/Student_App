from django.urls import path, include
from . import views
from django.contrib import admin

app_name = "student"


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("index", views.index, name="index"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path('student/<int:student_id>', views.student_by_id, name='student_by_id'),
    path("newstudent", views.creating_student, name="newstudent"),
    path("update/<int:student_id>", views.update_view, name="update"),
    path('api/login', views.login, name="api_login"),
    path('api/update/<int:student_id>', views.api_update, name="api_update"),
    path('api/delete/<int:student_id>', views.api_delete, name="api_delete"),



]
