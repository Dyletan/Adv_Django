from django.shortcuts import render, redirect
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin, IsAdminOrSelf
from rest_framework import viewsets
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('index')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('index')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Determine permissions based on action.
        - list, create: Admin only
        - retrieve, update, partial_update, destroy: Admin or self (user managing own profile)
        """
        if self.action in ['list', 'create']:
            permission_classes = [IsAdmin]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrSelf]
        else:
            permission_classes = [IsAdminOrSelf]
        return [permission() for permission in permission_classes]
    
def user_profile_view(request):
    return render(request, 'users/user_profile.html', {'user': request.user})

def user_list_view(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})