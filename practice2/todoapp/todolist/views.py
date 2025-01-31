from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Todo

def index(request):
    todos = Todo.objects.all()
    return render(request, "base.html", {"todo_list": todos})

@require_http_methods(["POST"])
def add(request):
    title = request.POST["title"]
    if not title:
        raise ValueError("Title cannot be empty.")
    Todo.objects.create(title=title)
    return redirect("index")

@require_http_methods(["GET"])
def update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.complete = not todo.complete
    todo.save()
    return redirect("index")

@require_http_methods(["GET"])
def delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return redirect("index")