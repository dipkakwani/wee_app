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

def dictFetchAll(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

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
        isSelf = 1 if userId == profileUserId else 0
        posts = {}
        # Fetch the mutual groupIds
        mutualGroupSql = "SELECT groupId_id FROM groupModule_joins j1\
                          WHERE EXISTS (SELECT groupId_id FROM groupModule_joins j2\
                          WHERE j1.userId_id=%s AND j2.userId_id=%s);"

        if isFriend or (userId == profileUserId):
            # Show all the private and public user posts and the posts in mutual groups made by the profile user.
            #FIXME: Not working when userId == profileUserId
            postsSql = "SELECT * FROM userModule_post WHERE posterId_id=%s AND groupId_id=NULL\
                        UNION\
                        SELECT * FROM userModule_post WHERE posterId_id=%s AND groupId_id IN (%s)"
            
        else:
            # Show all the public user posts and private mutual groups posts made by the profile user.
            postsSql = "SELECT * FROM userModule_post WHERE posterId_id=%s AND privacy='P'\
                        UNION\
                        SELECT * FROM userModule_post WHERE posterId_id=%s AND groupId_id IN (%s)"

        cursor.execute(postsSql, [profileUserId, profileUserId, mutualGroupSql, ])
        posts = dictFetchAll(cursor)
        return render(request, 'timeline.html', {'posts' : posts, 'isFriend' : isFriend , 'isSelf' : isSelf})
     
    return HttpResponseRedirect("/home")

#This view lets the user post something.
def newPost(request):
    userId = validateCookie(request)
    if userId:
        form = PostForm(user=userId)
        if request.method == 'POST':
            form = PostForm(request.POST, user=userId)
            if form.is_valid():
                content = request.POST.get('content')
                privacy = request.POST.get('privacy')
                group = request.POST.get('group')
                cursor = connection.cursor()
                sql = "INSERT INTO userModule_post (posterId_id, privacy, time, likes, comments, shares, content, groupId_id)\
                       VALUES (%s, %s, %s, 0, 0, 0, %s, %s)"
                if group == '-':
                    #FIXME: Integerity error, not allowing NULL in groupId_id.
                    cursor.execute(sql, [userId, privacy, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), content, 'NULL', ]) 
                else:
                    cursor.execute(sql, [userId, privacy, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), content, group, ])
                return HttpResponseRedirect("/timeline/" + userId)
            else:
                 return  render(request, 'newpost.html', {'form': form})

        return render(request, 'newpost.html', {'form': form})
    return HttpResponseRedirect("/home")

# Add or delete a friend
def friend(request, profileUserId):
    userId = validateCookie(request)
    if userId:
        # Check if the user with profileUserId exists or not
        cursor = connection.cursor()
        userSql = "SELECT 1 FROM userModule_user WHERE userId=%s"
        cursor.execute(userSql, [profileUserId, ])
        isUser = cursor.fetchall()
        if not isUser or userId == profileUserId:
            return HttpResponseRedirect("/notfound")

        friendSql = "SELECT 1 FROM userModule_friendship WHERE userA_id=%s AND userB_id=%s OR userA_id=%s AND userB_id=%s"
        cursor.execute(friendSql, [userId, profileUserId, profileUserId, userId, ])
        isFriend = cursor.fetchall()
        if isFriend:
            # Delete this friend
            deleteSql = "DELETE FROM userModule_friendship WHERE userA_id=%s AND userB_id=%s OR userA_id=%s AND userB_id=%s"
            cursor.execute(deleteSql, [userId, profileUserId, profileUserId, userId, ])
        else:
            # Add as a friend
            addSql = "INSERT INTO userModule_friendship (userA_id, userB_id, status) VALUES (%s, %s, 'R')"
            cursor.execute(addSql, [userId, profileUserId, ])
    return HttpResponseRedirect("/timeline/" + profileUserId)
