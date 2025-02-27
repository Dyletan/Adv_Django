from django.contrib import admin
from django.urls import path, reverse_lazy
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('delete/<int:id>/', views.delete_consume, name="delete"),
    path("chart-data/", views.chart_data, name="chart-data"),
    path('nutrient-summary-data/', views.nutrient_summary_data, name="nutrient-summary-data"),
    path("update-goals/", views.update_goals, name="update-goals"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="app/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name="logout"),
    path("add-food/", views.add_food, name="add-food"),
    path('line-chart-data/', views.line_chart_data, name="line-chart-data"),
]