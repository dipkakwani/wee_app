from django.contrib import admin
from userModule.models import User
from userModule.models import Friendship
from userModule.models import Following
from userModule.models import Post
from userModule.models import Like
from userModule.models import Comment
from userModule.models import Share
# Register your models here.

admin.site.register(User)
admin.site.register(Friendship)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Share)
