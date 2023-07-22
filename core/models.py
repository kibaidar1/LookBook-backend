import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode

UNISEX = 'us'
MALE = 'ml'
FEMALE = 'fl'
SEX_CHOICES = [(UNISEX, 'unisex'), (MALE, 'male'), (FEMALE, 'female')]

WHITE = 'wt'
RED = 'rd'
PINK = 'pk'
ORANGE = 'or'
YELLOW = 'yl'
LIGHT_GREEN = 'lgn'
GREEN = 'gn'
LIGHT_BLUE = 'lbl'
BLUE = 'bl'
PURPLE = 'pr'
BROWN = 'br'
BLACK = 'bk'

COLOUR_CHOICES = [(WHITE, 'white'), (RED, 'red'), (PINK, 'pink'), (ORANGE, 'orange'), (YELLOW, 'yellow'),
                  (LIGHT_GREEN, 'light_green'), (GREEN, 'green'), (LIGHT_BLUE, 'light_blue'), (PURPLE, 'purple'),
                  (BROWN, 'brown'), (BLACK, 'black')]


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
    colour = models.CharField(choices=COLOUR_CHOICES, null=True, blank=True, max_length=3)
    gender = models.CharField(choices=SEX_CHOICES, default=UNISEX, max_length=2)
    description = RichTextUploadingField()
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clothes')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)


class ClothesLink(models.Model):
    link = models.URLField()
    clothes = models.ForeignKey(Clothes, on_delete=models.CASCADE, related_name='links')


class Look(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    gender = models.CharField(choices=SEX_CHOICES, default=UNISEX, max_length=2)
    clothes = models.ManyToManyField(Clothes, related_name='looks')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='looks')

    class Meta:
        ordering = ['-created_at']

    def get_prev_look(self):
        try:
            return self.get_previous_by_created_at()
        except Look.DoesNotExist:
            return None

    def get_next_look(self):
        try:
            return self.get_next_by_created_at()
        except Look.DoesNotExist:
            return None

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)


class LookImages(models.Model):
    look = models.ForeignKey(Look, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name='images')


class Comment(models.Model):
    look = models.ForeignKey(Look, on_delete=models.CASCADE, related_name='comments', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(default=timezone.now)
    text = RichTextUploadingField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text
