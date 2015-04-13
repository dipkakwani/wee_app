from django.contrib import admin
from userModule.models import User
# Register your models here.

admin.site.register(User)
admin.site.register(Friendship)
admin.site.register(Following)
