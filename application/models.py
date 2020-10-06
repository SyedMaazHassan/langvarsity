from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
import random
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


class order(models.Model):
    order_date_time = models.DateTimeField(default = datetime.now())
    placed_by = models.ForeignKey(User, on_delete = models.CASCADE)
    text_type = models.CharField(max_length = 30)
    plane_text = models.TextField(blank = True, null = True, default = None)
    attachment = models.FileField(upload_to = "work", blank = True, null = True, default = None)
    special_note = models.TextField(blank = True, null = True, default = None)
    total_words = models.IntegerField(default = 0)
    file_type = models.CharField(max_length = 10, blank = True, null = True, default = None)
    alloted_to = models.ForeignKey(native_speaker, on_delete = models.CASCADE)
    is_new = models.BooleanField(default = True)
    is_confirmed = models.BooleanField(default = True)
    is_completed = models.BooleanField(default = False)

    def select_random_speaker(self):
        all_speakers = list(native_speaker.objects.all())
        
        if len(all_speakers) > 0:
            return random.choice(all_speakers)
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.pk:
            # selecting randome speaker to work
            self.alloted_to = self.select_random_speaker()

            if not self.alloted_to:
                self.is_confirmed = False

        super(order, self).save(*args, **kwargs)
