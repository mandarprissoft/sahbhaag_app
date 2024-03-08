from django.contrib import admin
from .models import CustomUser, Role, Center

admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(Center)
# Register your models here.
