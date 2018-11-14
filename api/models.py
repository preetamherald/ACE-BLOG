from django.db import models
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib import admin
from tastypie.models import create_api_key
from django_imgur.storage import ImgurStorage
from django.utils.text import slugify
from django.utils.encoding import smart_text
from django.conf import settings


AUTH_USER_MODEL = settings.AUTH_USER_MODEL


# Create your models here.

fs = FileSystemStorage(location='/media/photos')
STORAGE = ImgurStorage()

class PostModelManager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super(PostModelManager, self).all(*args, **kwargs).filter(active=True)
        return(qs)

class Posts(models.Model):
    title                = models.CharField(max_length=200, unique=True)
    tagline              = models.CharField(max_length=200,blank=True)
    author               = models.ForeignKey(
        User,
        null           = True,
        related_name   = 'entries',
        blank          = True,
        on_delete=models.SET_NULL
        )

    readtime             = models.PositiveIntegerField(blank=True, default=0)
    slug                 = models.SlugField(null=True, blank=True)
    energy               = models.PositiveIntegerField(blank=True, default=0)
    body                 = models.TextField()
    tags                 = models.CharField(max_length=200,blank=True)
    created_at           = models.DateTimeField(auto_now_add=True)
    last_modified        = models.DateTimeField(auto_now=True)
    last_modified_by     = models.ForeignKey(
        User,
        null           = True,
        related_name   = 'entry_modifiers',
        blank          = True,
        on_delete=models.SET_NULL
        )

    active               = models.BooleanField(default=True)
    image                = models.ImageField(
        upload_to      = 'photos',
        storage        = STORAGE,
        null           = True,
        blank          = True,
        max_length     = None
        )

    objects = PostModelManager()

    def __str__(self):
        return smart_text(self.title)

    def save(self, *args, **kwargs):
        print("Hello There")
        if not self.slug:
            self.slug = slugify(self.title)
        super(Posts, self).save(*args, **kwargs)


class UserDetail(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, related_name='user_detail', on_delete=models.CASCADE)
    image                = models.ImageField(
        upload_to      = 'photos',
        storage        = STORAGE,
        null           = True,
        blank          = True,
        max_length     = None
        )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return smart_text(self.user)


def create_user_detail(sender, instance, created, **kwargs):
    """
    A signal for hooking up automatic ``User Detail`` creation.
    """
    if kwargs.get('raw', False) is False and created is True:
        UserDetail.objects.create(user=instance)





models.signals.post_save.connect(create_api_key, sender=User)
models.signals.post_save.connect(create_user_detail, sender=User)
