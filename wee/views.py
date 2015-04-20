from django.http import HttpResponse
from django.conf import settings
from userModule.models import User
from userModule.models import Post
from userModule.models import Friendship
from userModule.models import Following
from userModule.models import Share
from userModule.models import Like
from userModule.models import Comment
from groupModule.models import Group
from groupModule.models import Join
from userModule.forms import PostForm
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
        if userId           # Valid user id?
            if request.method == 'POST':
                form = PostForm(request.POST)
                if form.is_valid():
                    content = request.POST.get('content')
                    #TODO: Insert the data in post model.
                else:
                    #TODO:Render the post template with errors.
            else:
                #TODO: Render the post template.

        else:       # Invalid user id
            return HttpResponseRedirect("/home")
    return HttpResponseRedirect("/home")
