from django.urls import path
from .views import signup_view, login_view, home_view, logout_view
from django.contrib.auth import views as auth_views
from .views import store_message,get_messages
from .views import get_authenticated_user, get_users, store_message
from . import views

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('store_message/', store_message, name='store_message'),
    path('get_messages/<str:username>/', get_messages, name='get_messages'),
    path("get_authenticated_user/", get_authenticated_user, name="get_authenticated_user"),
    path("get_users/", get_users, name="get_users"),
    path('chat/', views.chat, name='chat'),

]
