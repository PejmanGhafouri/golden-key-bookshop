from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Create your models here.

# Create your models here.
class User(AbstractUser):
	email = models.EmailField(unique=True, verbose_name='ایمیل')
	is_author = models.BooleanField(default=False, verbose_name="وضعیت نویسندگی")
