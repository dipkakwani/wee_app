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

def timeline(request, profileUserId):
    # Check which user is currently logged in. Only a logged in user can view other users' profile.
    userId = validateCookie(request)
    if userId:
        cursor = connection.cursor()

        # Check if the user with profileUserId exists or not
        userSql = "SELECT 1 FROM userModule_user WHERE userId=%s"
        cursor.execute(userSql, [profileUserId, ])
        isUser = cursor.fetchall()
        if not isUser:
            return HttpResponseRedirect("/notfound")

        #Check if the logged in user is a friend or not
        friendSql = "SELECT 1 FROM userModule_friendship WHERE userA_id=%s AND userB_id=%s OR userA_id=%s AND userB_id=%s"
        cursor.execute(friendSql, [userId, profileUserId, profileUserId, userId, ])
        isFriend = cursor.fetchall()
        #TODO: Complete this view.
        if isFriend or (userId == profileUserId):
            # Show all the private posts and the posts in mutual groups made by the profile user.
            # Fetch the mutual groupIds
            return HttpResponse("private")
        else:
            # Show all the public posts
            return HttpResponse("Public")
        
    return HttpResponseRedirect("/home")

#This view lets the user post something.
def newPost(request):
    userId = validateCookie(request)
    if userId:
        form = PostForm(userId)
        if request.method == 'POST':
            form = PostForm(request.POST, userId)
            if form.is_valid():
                content = request.POST.get('content')
                privacy = request.POST.get('privacy')
                group = request.POST.get('group')
                #TODO:Check if the post is a group post and store the data in post table.
                pass
        return render(request, 'newpost.html', {'form': form})

    return HttpResponseRedirect("/home")
