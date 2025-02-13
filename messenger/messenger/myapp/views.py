from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Dialog, Message
from .forms import NewDialogForm
from django.contrib.auth.models import User



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически входим после регистрации
            return redirect('home')  # Перенаправление на главную страницу
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
                return redirect('home')  # Перенаправление на главную страницу
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа после выхода


def success(request):
    return render(request, 'myapp/success.html')


@login_required
def home(request):
    # Получаем все диалоги текущего пользователя
    dialogs = Dialog.objects.filter(participants=request.user).order_by('-created_at')

    # Обработка создания нового диалога
    if request.method == 'POST':
        form = NewDialogForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message_text = form.cleaned_data['message']

            # Находим пользователя по email
            try:
                recipient = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error('email', 'Пользователь с таким email не найден.')
            else:
                # Создаем новый диалог
                dialog = Dialog.objects.create()
                dialog.participants.add(request.user, recipient)
                dialog.save()

                # Создаем первое сообщение
                Message.objects.create(
                    dialog=dialog,
                    sender=request.user,
                    text=message_text
                )

                return redirect('home')
    else:
        form = NewDialogForm()

    return render(request, 'myapp/home.html', {
        'dialogs': dialogs,
        'form': form,
    })


@login_required
def chat(request):
    # Получаем все диалоги текущего пользователя
    dialogs = Dialog.objects.filter(participants=request.user).order_by('-created_at')

    # Добавляем информацию о собеседнике для каждого диалога
    dialogs_with_recipient = []
    for dialog in dialogs:
        recipient = dialog.participants.exclude(id=request.user.id).first()
        dialogs_with_recipient.append({
            'dialog': dialog,
            'recipient': recipient,
        })

    # Обработка создания нового диалога
    if request.method == 'POST':
        form = NewDialogForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message_text = form.cleaned_data['message']

            # Находим пользователя по email
            try:
                recipient = User.objects.get(email=email)
            except User.DoesNotExist:
                form.add_error('email', 'Пользователь с таким email не найден.')
            else:
                # Создаем новый диалог
                dialog = Dialog.objects.create()
                dialog.participants.add(request.user, recipient)
                dialog.save()

                # Создаем первое сообщение
                Message.objects.create(
                    dialog=dialog,
                    sender=request.user,
                    text=message_text
                )

                return redirect('chat')
    else:
        form = NewDialogForm()

    return render(request, 'myapp/chat.html', {
        'dialogs_with_recipient': dialogs_with_recipient,
        'form': form,
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


