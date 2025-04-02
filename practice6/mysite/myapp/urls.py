from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path("add_category/", views.add_category, name="add_category"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('group_expenses/', views.group_expenses_list, name='group_expense_list'),
    path('group_expenses/create/', views.create_group_expense, name='create_group_expense'),
]