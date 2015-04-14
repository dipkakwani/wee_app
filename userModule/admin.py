from django.contrib import admin
from userModule.models import User
from userModule.models import Friendship
from userModule.models import Following
# Register your models here.

admin.site.register(User)
admin.site.register(Friendship)
admin.site.register(Following)
