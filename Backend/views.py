from django.shortcuts import render



def frontend_page(request):
    return render(request, 'index.html')  

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')