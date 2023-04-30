from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if username is None:
            raise TypeError('Users must have a username')

        if email is None:
            raise TypeError('Users must have an email address')

        if password is None:
            raise TypeError('Users must have a password')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_staff_user(self, username, email, password):
        if username is None:
            raise TypeError('Superuser must have a username')

        if email is None:
            raise TypeError('Superuser must have an email address')

        if password is None:
            raise TypeError('Superuser must have a password')

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if username is None:
            raise TypeError('Superuser must have a username')

        if email is None:
            raise TypeError('Superuser must have an email address')

        if password is None:
            raise TypeError('Superuser must have a password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(unique=True, validators=[validators.validate_email], db_index=True)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


class Clothes(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    image = models.ImageField()
    link = models.URLField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Style(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    image = models.ImageField()
    clothes = models.ManyToManyField(Clothes, related_name='styles')
    slug = models.SlugField(unique=True)
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    def get_prev_style(self):
        try:
            return self.get_previous_by_created_at()
        except Style.DoesNotExist:
            return None

    def get_next_style(self):
        try:
            return self.get_next_by_created_at()
        except Style.DoesNotExist:
            return None

    def __str__(self):
        return self.name


class Comment(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='comments', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(default=timezone.now)
    text = RichTextUploadingField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text
