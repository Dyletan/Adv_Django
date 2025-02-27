from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'api/users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('profile-html/', user_profile_view, name='user-profile-html'),
    path('users-list-html/', user_list_view, name='user-list-html'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]