from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .forms import MessageForm
from django.contrib.auth.decorators import login_required
from .models import Dialog, Message
from .forms import NewDialogForm

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


