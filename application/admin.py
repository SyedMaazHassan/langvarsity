from django.contrib import admin
from .models import *

# Register your models here.

class native_show(admin.ModelAdmin):
    list_display = [
        'which_user',
        'g_passport',
        'isAccepted',
        # 'org_1',
        # 'year_1',
        # 'type_1',
        # 'org_2',
        # 'year_2',
        # 'type_2',
        # 'org_3',
        # 'year_3',
        # 'type_3',
        # 'org_4',
        # 'year_4',
        # 'type_4'
    ]

    list_editable = [
        'isAccepted'
    ]


admin.site.register(native_speaker, native_show)