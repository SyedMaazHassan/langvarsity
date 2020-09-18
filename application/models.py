from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
# Create your models here.

class native_speaker(models.Model):
    which_user = models.ForeignKey(User, on_delete = models.CASCADE)
    g_passport = models.FileField(upload_to = 'docs')
    isAccepted = models.BooleanField(default = False)
    
    org_1 = models.CharField(max_length = 100)
    year_1 = models.IntegerField()
    type_1 = models.CharField(max_length = 100)

    org_2 = models.CharField(max_length = 100, null = True, default = None, blank = True)
    year_2 = models.IntegerField(null = True, default = None, blank = True)
    type_2 = models.CharField(max_length = 100, null = True, default = None, blank = True)

    org_3 = models.CharField(max_length = 100, null = True, default = None, blank = True)
    year_3 = models.IntegerField(null = True, default = None, blank = True)
    type_3 = models.CharField(max_length = 100, null = True, default = None, blank = True)

    org_4 = models.CharField(max_length = 100, null = True, default = None, blank = True)
    year_4 = models.IntegerField(null = True, default = None, blank = True)
    type_4 = models.CharField(max_length = 100, null = True, blank = True, default = None)