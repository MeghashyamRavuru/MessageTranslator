from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from django.http import JsonResponse
from django.db import connection
from .models import create_user_table


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful. Please log in.")
            return redirect('login')
        else:
            print("Signup failed due to errors:", form.errors)  # Debugging line
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")  # Adds red-colored messages
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please sign up if you don't have an account.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'index.html')



def store_message(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        message = request.POST.get("message", "").strip()

        if not username or not message:
            return JsonResponse({"error": "Username and message are required"}, status=400)

        # Create the user's table if not exists
        table_name = create_user_table(username)

        # Insert the message
        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table_name} (message) VALUES (%s)", [message])

        return JsonResponse({"success": f"Message stored in {table_name} table"})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def get_messages(request, username):
    table_name = username.replace(" ", "_").lower()
    
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT message, timestamp FROM {table_name} ORDER BY timestamp DESC")
        messages = cursor.fetchall()

    return JsonResponse({"messages": messages})



