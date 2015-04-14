from django.contrib import admin
from groupModule.models import Group
from groupModule.models import Joined
from groupModule.models import Post

# Register your models here.

admin.site.register(Group)
admin.site.register(Joined)
admin.site.register(Post)
