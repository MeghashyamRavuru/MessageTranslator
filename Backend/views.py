from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from django.http import JsonResponse
from django.db import connection
from .models import create_user_table
from django.contrib.auth.decorators import login_required


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



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import connection
from .models import CustomUser, create_user_table, translator
import json

@csrf_exempt
def store_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sender_username = data.get("sender", "").strip()
        receiver_username = data.get("receiver", "").strip()
        message = data.get("message", "").strip()

        if not sender_username or not receiver_username or not message:
            return JsonResponse({"error": "All fields are required"}, status=400)

        sender = get_object_or_404(CustomUser, username=sender_username)
        receiver = get_object_or_404(CustomUser, username=receiver_username)
        table_name = create_user_table(sender_username)

        translated_text = translator.translate(message, dest=receiver.language).text

        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table_name} (sender, receiver, message, translated_message) VALUES (%s, %s, %s, %s)", [sender_username, receiver_username, message, translated_text])

        return JsonResponse({"success": "Message stored successfully", "translated_message": translated_text})
    
    return JsonResponse({"error": "Invalid request"}, status=400)


def get_messages(request, username):
    table_name = username.replace(" ", "_").lower()
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT sender, receiver, message, translated_message, timestamp FROM {table_name} ORDER BY timestamp DESC")
        messages = cursor.fetchall()

    return JsonResponse({"messages": messages})

@login_required
def get_authenticated_user(request):
    return JsonResponse({"username": request.user.username})


@login_required
def get_users(request):
    users = CustomUser.objects.values_list("username", flat=True)
    return JsonResponse({"users": list(users)})

def chat(request):
    return render(request, 'chat.html')