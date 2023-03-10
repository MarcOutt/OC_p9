from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    """Gestionnaire d'utilisateur personnalisé"""
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Vous devez entrer un pseudo")
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    """Modèle pour créer des utilisateurs"""
    username = models.CharField(max_length=63, unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    objects = MyUserManager()
    follows = models.ManyToManyField('self', symmetrical=False, verbose_name='suit')

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Ticket(models.Model):
    """Modèle pour la création d'un ticket et à une relation avec le CustomUser """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UsersFollows(models.Model):
    """Permet de créer une relation de plusieurs à plusieurs entre les instances de CustomUser"""
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')


class Review(models.Model):
    """Modèle pour créer une review avec une relation de ForeignKey avec CustomUser et une autre avec Ticket"""
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField(verbose_name="Note")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.TextField(max_length=8192, verbose_name="Commentaire")
    time_created = models.DateTimeField(auto_now_add=True)
