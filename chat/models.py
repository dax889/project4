from django.db import models


class Message(models.Model):
    user = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.content[:50]}"
