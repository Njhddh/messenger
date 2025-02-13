from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


class Dialog(models.Model):
    participants = models.ManyToManyField(User, related_name='dialogs')  # Участники диалога
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания диалога

    def __str__(self):
        return f"Диалог {self.id}"


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='messages')  # Диалог, к которому относится сообщение
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # Отправитель сообщения
    text = models.TextField()  # Текст сообщения
    timestamp = models.DateTimeField(auto_now_add=True)  # Время отправки сообщения

    def __str__(self):
        return f"Сообщение от {self.sender.username} в {self.timestamp}"