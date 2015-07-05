from django.db import models
from django.contrib.auth.models import AbstractUser


class PoolUser(AbstractUser):

    """ Model for Material Pool User """

    is_subscribed = models.BooleanField(default=False)
