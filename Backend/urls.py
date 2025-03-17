from django.urls import path
from Backend.views import frontend_page,login_view, signup_view


urlpatterns = [
    path('', frontend_page, name='frontend_page'),  
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
]