from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from django.http import JsonResponse
from django.db import connection
#from .models import create_user_table
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
from .models import CustomUser, translator
import json
from googletrans import Translator
from .models import CustomUser, Message

translator = Translator()

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

        # Translate the message to receiver's language
        translated_text = translator.translate(message, dest=receiver.language).text

        # Store message in database
        Message.objects.create(sender=sender, receiver=receiver, message=message, translated_message=translated_text)

        return JsonResponse({"success": "Message stored successfully", "translated_message": translated_text})

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_messages(request, username):
    current_user = request.user
    chat_user = get_object_or_404(CustomUser, username=username)

    # Fetch messages where the user is either sender or receiver
    messages = Message.objects.filter(
        sender=current_user, receiver=chat_user
    ) | Message.objects.filter(
        sender=chat_user, receiver=current_user
    ).order_by("timestamp")

    message_list = [
        {
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "message": msg.message,
            "translated_message": msg.translated_message,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for msg in messages
    ]

    return JsonResponse({"messages": message_list})


@login_required
def get_authenticated_user(request):
    return JsonResponse({"username": request.user.username})


@login_required
def get_users(request):
    users = CustomUser.objects.values_list("username", flat=True)
    return JsonResponse({"users": list(users)})


def chat(request):
    return render(request, 'chat.html')