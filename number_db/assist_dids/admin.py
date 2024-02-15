from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Status)
admin.site.register(Voice_Carrier)
admin.site.register(SMS_Carrier)
admin.site.register(SMS_Type)
admin.site.register(Term_Location)