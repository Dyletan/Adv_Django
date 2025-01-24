from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from .models import User, Project, Category, Priority, Task 
from .serializers import UserSerializer, ProjectSerializer, CategorySerializer, PrioritySerializer, TaskSerializer
from rest_framework.filters import SearchFilter 
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdmin, IsManager, IsEmployee  
from rest_framework.exceptions import PermissionDenied

class UserViewSet(ModelViewSet): 
    queryset = User.objects.all() 
    serializer_class = UserSerializer 
    permission_classes = [IsAdmin] 

class ProjectViewSet(ModelViewSet): 
    queryset = Project.objects.all() 
    serializer_class = ProjectSerializer
    permission_classes = [IsManager]

class CategoryViewSet(ModelViewSet): 
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer 

class PriorityViewSet(ModelViewSet): 
    queryset = Priority.objects.all() 
    serializer_class = PrioritySerializer 

class TaskViewSet(ModelViewSet): 
    queryset = Task.objects.all() 
    serializer_class = TaskSerializer 
    filter_backends = [DjangoFilterBackend, SearchFilter] 
    filterset_fields = ['project', 'priority', 'category'] 
    search_fields = ['title', 'description']
    permission_classes = [IsEmployee]
    
    def perform_create(self, serializer): 
        serializer.save()
    
    def retrieve(self, request, *args, **kwargs):
        task = self.get_object()

        if request.user.role == 'employee' and task.assignee != request.user:
            raise PermissionDenied("You do not have permission to view this task.")
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        task = self.get_object()

        if self.request.user.role == 'employee' and task.assignee != self.request.user:
            raise PermissionDenied("You cannot update tasks not assigned to you.")
        serializer.save()