from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(null=True, unique=True)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name='friends_with', blank=True)

    friend_requests = models.ManyToManyField('self', through='FriendRequest', symmetrical=False, related_name='friends_requests', blank=True)
    
    full_name = models.CharField(max_length=255, default='None')

    bio = models.TextField(null=True, blank=True, default="No Bio For Now")
    avatar = models.ImageField(null=True, default='avatar.svg')

    # ანუ იუზერნეიმ ფიელდ იქნება ემაილი ეხლა
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def save(self, *args, **kwargs):
        self.username = self.email  # Ensure username stays synced with email
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
    
class Friendship(models.Model):
    # Intermediary table for the friendship relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_friendships')
    # Add any additional fields for the friendship relationship here (e.g., date added)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.friend.email}'

class FriendRequest(models.Model):
    """A model to represent a sent or received friend request."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friendrequest')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friendreciever')

    rejected = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.email} - {self.receiver.email}'