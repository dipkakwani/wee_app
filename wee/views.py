from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from userModule.models import User
from userModule.models import Post
from userModule.models import Friendship
from userModule.models import Following
from userModule.models import Share
from userModule.models import Like
from userModule.models import Comment
from groupModule.models import Group
from groupModule.models import Joins
from wee.forms import PostForm
from userModule.security import *

from datetime import datetime

def newsfeed(request):
    #TODO: Fetch the posts from currently logged in user's network
    pass

def timeline(request):
    # Check which user is currently logged in. Only a logged in user can view other users' profile.
    if "sessionId" in request.COOKIES:
        userId = checkSecureVal(request.COOKIES["sessionId"])
        if userId:
            pass
        else:
            return HttpResponseRedirect("/home")
    else:
        return HttpResponseRedirect("/home")

#This view lets the user post something.
def newPost(request):
    if "sessionId" in request.COOKIES:
        userId = checkSecureVal(request.COOKIES["sessionId"])
        if userId:           # Valid user id?
            form = PostForm(userId)
            if request.method == 'POST':
                form = PostForm(request.POST, userId)
                if form.is_valid():
                    content = request.POST.get('content')
                    privacy = request.POST.get('privacy')
                    group = request.POST.get('group')
                    #TODO: Check if the post is a group post and store the data in post table.
                    pass
                else:
                    return render(request, 'newpost.html', {'form' : form})
            else:
                return render(request, 'newpost.html', {'form': form})

        else:       # Invalid user id
            return HttpResponseRedirect("/home")
    return HttpResponseRedirect("/home")
