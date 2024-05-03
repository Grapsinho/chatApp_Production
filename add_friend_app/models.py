from django.db import models
from users.models import User

class Friendship(models.Model):
    # Intermediary table for the friendship relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_friendships')
    # Add any additional fields for the friendship relationship here (e.g., date added)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.friend.email}'
