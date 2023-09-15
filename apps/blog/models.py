from django.db import models
from apps.utils.models import BaseModel


class Product(BaseModel):
    name = models.TextField(max_length=255)
