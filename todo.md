## create venv

pip install django

##create project
django-admin startproject todoapp

##create app
py manage.py startapp todolist

##add app in apps list in settings.py

##add urls.py file in todolist
from django.urls import path

from . import views


urlpattern = [
    path('', views.index, name="index")
]


##add in urls.py in todoapp
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todolist.urls'))
]


##create "templates" in base todoapp with base.html file 
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css">
    <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"></script>
</head>

<body>
    <div style="margin-top: 50px;" class="ui container">
        <h1 class="ui center aligned header">To Do App</h1>

        <form class="ui form" action="/add" method="post">
            {% csrf_token %}
            <div class="field">
                <label>Todo Title</label>
                <input type="text" name="title" placeholder="Enter Todo..."><br>
            </div>
            <button class="ui blue button" type="submit">Add</button>
        </form>

        <hr>

        {% for todo in todo_list %}
        <div class="ui segment">
            <p class="ui big header">{{ todo.id }} | {{ todo.title }}</p>

            {% if todo.complete == False %}
            <span class="ui gray label">Not Complete</span>
            {% else %}
            <span class="ui green label">Completed</span>
            {% endif %}

            <a class="ui blue button" href="/update/{{ todo.id }}">Update</a>
            <a class="ui red button" href="/delete/{{ todo.id }}">Delete</a>
        </div>
        {% endfor %}
    </div>
</body>

</html>


## in settings.py add templates dirs as templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {

##create "Todo" model in models.py 

from django.db import models

# Create your models here.
class Todo(models.Model):
    title=models.CharField(max_length=350)
    complete=models.BooleanField(default=False)

    def __str__(self):
        return self.title

##create view for listing in views,py (todolist)
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .models import Todo

# Create your views here.
def index(request):
    todos = Todo.objects.all()
    return render(request, "base.html", {"todo_list": todos})

## create add start migrations 
py manage.py makemigrations
py manage.py migrate

## create superuser 
py manage.py createsuperuser

##register Todo model in todolist admin.py
from django.contrib import admin
from .models import Todo

admin.site.register(Todo)

##add view for listing in views,py (todolist)
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .models import Todo

# Create your views here.
def index(request):
    todos = Todo.objects.all()
    return render(request, "base.html", {"todo_list": todos})

## add other actions in views.py
@require_http_methods(["POST"])
def add(request):
    # if request.method == "POST":
    title = request.POST["title"]
    todo = Todo(title=title)
    todo.save()
    return redirect("index")


def update(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.complete = not todo.complete
    todo.save()
    return redirect("index")


def delete(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return redirect("index")

##update the urlspatterns in urls.py (todolist)
urlpatterns = [
    path('', views.index, name="index"),
    path('add', views.add, name="add"),
    path('delete/<int:todo_id>', views.delete, name="delete"),
    path('update/<int:todo_id>', views.update, name="update"),
]