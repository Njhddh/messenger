from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Dialog
from .forms import MessageForm


@login_required
def chat(request, dialog_id=None):
    # Получаем все диалоги текущего пользователя
    dialogs = Dialog.objects.filter(participants=request.user)

    # Если выбран конкретный диалог
    dialog = None
    messages = []
    if dialog_id:
        dialog = get_object_or_404(Dialog, id=dialog_id, participants=request.user)
        messages = dialog.messages.all().order_by('timestamp')

    # Обработка отправки сообщения
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            if dialog:
                message = form.save(commit=False)
                message.dialog = dialog
                message.sender = request.user
                message.save()
                return redirect('chat', dialog_id=dialog.id)
    else:
        form = MessageForm()

    return render(request, 'myapp/chat.html', {
        'dialogs': dialogs,
        'dialog': dialog,
        'messages': messages,
        'form': form,
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'myapp/home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = RegistrationForm()

    return render(request, 'myapp/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправление на главную страницу после входа
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа после выхода


def success(request):
    return render(request, 'myapp/success.html')
