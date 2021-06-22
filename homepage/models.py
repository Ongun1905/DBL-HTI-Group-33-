# Import settings to allow BASE_DIR to be used
from django.conf import settings

# Django imports
from django.db import models


# Create your models here.
class File(models.Model):
  file = models.FileField()