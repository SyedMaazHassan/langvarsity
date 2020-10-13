from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
import random
import hashlib as hl
import six, base64

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

    # -1 => CANCELLED
    # 0 => IN PROGRESS
    # 1 => DELIVERED
    # 2 => ASK FOR REVISION
    # 3 => COMPLETED
    order_status =  models.CharField(max_length = 20, default = "IN-PROCESS")


    def select_random_speaker(self):
        all_speakers = list(native_speaker.objects.filter(isAccepted = True))
        
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

    def __str__(self):
        return "ID = {},  Date = {},   Placed by = {},  alloted to = {}".format(self.id, self.order_date_time, self.placed_by, self.alloted_to)


class allMsg(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "sender_user")
    receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "receiver_user")
    message = models.TextField()
    moment = models.DateTimeField(default = datetime.now())

    def generate_code(self):
        strs = self.sender.username + self.receiver.username
        print(strs)
        code_hash = hl.md5(strs.encode())
        return code_hash.hexdigest()

    def encode(self, key, string):
        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = ''.join(encoded_chars)
        encoded_string = encoded_string.encode('latin') if six.PY3 else encoded_string
        return base64.urlsafe_b64encode(encoded_string).rstrip(b'=')

    def save(self, *args, **kwargs):
        if not self.pk:
            our_key = self.generate_code()
            self.message = self.encode(our_key, self.message)
            
        super(allMsg, self).save(*args, **kwargs)


class deliveries(models.Model):
    revised_file = models.FileField(upload_to = 'delivery')
    order = models.ForeignKey(order, on_delete = models.CASCADE)
    order_date_time = models.DateTimeField(default = datetime.now())

    def save(self, *args, **kwargs):
        if not self.pk:
            self.order.order_status = "DELIVERED"
            self.order.save()
            
        super(deliveries, self).save(*args, **kwargs)