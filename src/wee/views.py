from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from userModule.models import *
from groupModule.models import *
from wee.forms import *
from userModule.security import *

from datetime import datetime

def dictFetchAll(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

def dictFetchOne(cursor):
    """Returns a single row from a cursor as a dict"""
    desc = cursor.description
    return dict(zip([col[0] for col in desc], cursor.fetchone()))

def newsfeed(request):
    userId = validateCookie(request)    # Is the user logged in?
    if not userId:
        return HttpResponseRedirect("/home")

    # Fetch the posts from user(currently logged in), friends, following users and groups.
    postsSql = "  select distinct * from\
                (select p.postId, p.posterId_id, p.likes, p.comments, p.time, p.groupId_id,p.shares, p.content,p.privacy from userModule_post p\
                NATURAL JOIN (select userA_id as posterId_id from userModule_friendship where userB_id=%s  and status='A'\
                union select userB_id as posterId_id from userModule_friendship where userA_id=%s and status='A'\
                ) as friends_posts where p.groupId_id is null\
                UNION\
                select p.postId, p.posterId_id, p.likes, p.comments, p.time, p.groupId_id,p.shares, p.content,p.privacy from userModule_post p\
                NATURAL JOIN (select userB_id as posterId_id from userModule_following where userA_id=%s) as following_posts\
                where p.privacy='P' and p.groupId_id is null\
                UNION\
                select p.postId, p.posterId_id, p.likes, p.comments, p.time, p.groupId_id,p.shares, p.content,p.privacy from userModule_post p\
                where posterId_id=%s\
                UNION\
                select p.postId, p.posterId_id, p.likes, p.comments, p.time, p.groupId_id,p.shares, p.content,p.privacy from userModule_post p\
                NATURAL JOIN (select groupId_id as groupId_id from groupModule_joins where userId_id=%s and status='A')\
                as group_posts\
                ) as s\
                ORDER BY time desc;"
    cursor = connection.cursor()
    cursor.execute(postsSql, [userId, ] * 5)
    posts = dictFetchAll(cursor)

    # Fetch the user name and group name (if any) from groupId_id to send to the template.
    for post in posts:
        userSql = "SELECT name FROM userModule_user WHERE userId=%s"
        cursor.execute(userSql, [post['posterId_id'], ])
        post['name'] = cursor.fetchone()[0].encode('ascii')
        post['groupName'] = ""
        if post['groupId_id']:
            groupNameSql = "SELECT groupName from groupModule_group where groupId=%s"
            cursor.execute(groupNameSql, [post['groupId_id'], ])
            post['groupName'] = cursor.fetchone()[0].encode('ascii')

    return render(request, 'newsfeed.html', {'posts' : posts, 'userId' : userId, })

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

        # Check if the user is friend or not.
        friendSql = "SELECT 1 FROM userModule_friendship WHERE userA_id=%s AND userB_id=%s AND status='A'OR\
                     userA_id=%s AND userB_id=%s AND status='A'"
        cursor.execute(friendSql, [userId, profileUserId, profileUserId, userId, ])
        isFriend = cursor.fetchall()

        # Check if the user has sent friend request
        if not isFriend:
            friendRequestSql = "SELECT 1 FROM userModule_friendship WHERE userA_id=%s AND userB_id=%s OR\
                                userA_id=%s AND userB_id=%s"
            cursor.execute(friendRequestSql, [userId, profileUserId, profileUserId, userId, ])
            friendRequest = cursor.fetchall()
        else:
            friendRequest = ()

        # Check if the logged in user is following the profileUser
        followingSql = "SELECT 1 FROM userModule_following WHERE userA_id=%s AND userB_id=%s"
        cursor.execute(followingSql, [userId, profileUserId, ])
        isFollowing = cursor.fetchall()

        isSelf = 1 if userId == profileUserId else 0
        posts = {}

        if isFriend or isSelf:
            # Show all the private and public user posts and the posts in mutual groups made by the profile user.
            postsSql = "SELECT * FROM ((SELECT * FROM userModule_post WHERE posterId_id=%s AND groupId_id is NULL)\
                        UNION\
                        (SELECT * FROM userModule_post WHERE posterId_id=%s AND groupId_id IN (SELECT groupId_id FROM groupModule_joins j1\
                          WHERE EXISTS (SELECT groupId_id FROM groupModule_joins j2\
                          WHERE j1.userId_id=%s AND j1.status='A' AND j2.userId_id=%s AND j2.status='A')))) temp ORDER BY time desc;"

        else:
            # Show all the public user posts and private mutual groups posts made by the profile user.
            postsSql = "SELECT * FROM ((SELECT * FROM userModule_post WHERE posterId_id=%s AND privacy='P')\
                        UNION\
                        (SELECT * FROM userModule_post WHERE posterId_id=%s AND groupId_id IN (SELECT groupId_id FROM groupModule_joins j1\
                          WHERE EXISTS (SELECT groupId_id FROM groupModule_joins j2\
                          WHERE j1.userId_id=%s AND j1.status='A' AND j2.userId_id=%s AND j2.status='A')))) temp ORDER BY time desc;"

        cursor.execute(postsSql, [profileUserId, ] * 4)
        posts = dictFetchAll(cursor)

        # Fetch the group name (if any) from groupId_id to send to the template.
        for post in posts:
            post['groupName'] = ""
            if post['groupId_id']:
                groupNameSql = "SELECT groupName from groupModule_group where groupId=%s"
                cursor.execute(groupNameSql, [post['groupId_id'], ])
                post['groupName'] = cursor.fetchone()[0].encode('ascii')

        # Fetch information of the user.
        userInfoSql = "SELECT name, dob, sex, profilePic, school, college, companyName, status, profession, website\
                       FROM userModule_user WHERE userId=%s"
        cursor.execute(userInfoSql, [profileUserId, ])
        user = dictFetchOne(cursor)
        user['sex'] = "Male" if user['sex'] == 'M' else "Female"
        if user['status'] == "M":
            user['status'] = "Married"
        elif user['status'] == "U":
            user['status'] = "Unmarried"

        return render(request, 'timeline.html', {'posts' : posts, 'isFriend' : isFriend , 'isFollowing': isFollowing,\
                'isSelf' : isSelf, 'len' : len(posts), 'userId': userId, 'user' : user, 'friendRequest' : friendRequest})

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

                if group == '-':
                    sql = "INSERT INTO userModule_post (posterId_id, privacy, time, likes, comments, shares, content)\
                           VALUES (%s, %s, %s, 0, 0, 0, %s)"
                    cursor.execute(sql, [userId, privacy, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), content, ])
                else:
                    sql = "INSERT INTO userModule_post (posterId_id, privacy, time, likes, comments, shares, content, groupId_id)\
                           VALUES (%s, %s, %s, 0, 0, 0, %s, %s)"
                    cursor.execute(sql, [userId, privacy, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), content, group, ])

                return HttpResponseRedirect("/timeline/" + userId)

        return render(request, 'newpost.html', {'form': form, 'userId' : userId})
    return HttpResponseRedirect("/home")

# Add or delete a friend
def updateFriend(request,profileUserId,change):
    userId = validateCookie(request)
    if  change != 'A' and change != 'D' or not userId:
        return HttpResponseRedirect('/notfound')

    # Check if the user with profileUserId exists or not
    cursor = connection.cursor()
    userSql = "SELECT 1 FROM userModule_user WHERE userId=%s"
    cursor.execute(userSql, [profileUserId, ])
    isUser = cursor.fetchall()
    if not isUser or userId == profileUserId:
        return HttpResponseRedirect("/notfound")

    friendSql = "SELECT 1 FROM userModule_friendship WHERE (userA_id=%s AND userB_id=%s) OR (userA_id=%s AND userB_id=%s)"
    cursor.execute(friendSql, [userId, profileUserId, profileUserId, userId, ])
    isFriend = cursor.fetchall()
    if isFriend:
        if change == 'D':
            # Delete this friend
            deleteSql = "DELETE FROM userModule_friendship WHERE (userA_id=%s AND userB_id=%s) OR (userA_id=%s AND userB_id=%s)"
            cursor.execute(deleteSql, [userId, profileUserId, profileUserId, userId, ])
        else:
            # Accept the friend request
            acceptSql = "UPDATE userModule_friendship SET status='A' WHERE userA_id=%s AND userB_id=%s"
            cursor.execute(acceptSql, [profileUserId, userId, ])
    else:
            # Add as a friend
            addSql = "INSERT INTO userModule_friendship (userA_id, userB_id, status) VALUES (%s, %s, 'R')"
            cursor.execute(addSql, [userId, profileUserId, ])
    return HttpResponseRedirect("/timeline/" + profileUserId)

def updateFollow(request, profileUserId):
    userId = validateCookie(request)
    if userId:
        # Check if the user with profileUserId exists or not
        cursor = connection.cursor()
        userSql = "SELECT 1 FROM userModule_user WHERE userId=%s"
        cursor.execute(userSql, [profileUserId, ])
        isUser = cursor.fetchall()
        if not isUser or userId == profileUserId:
            return HttpResponseRedirect("/notfound")

        followSql = "SELECT 1 FROM userModule_following WHERE userA_id=%s AND userB_id=%s"
        cursor.execute(followSql, [userId, profileUserId, ])
        isFollowing = cursor.fetchall()
        if isFollowing:
            # Unfollow the user
            unfollowSql = "DELETE FROM userModule_following WHERE userA_id=%s AND userB_id=%s"
            cursor.execute(unfollowSql, [userId, profileUserId, ])
        else:
            # Follow the user
            followSql = "INSERT INTO userModule_following (userA_id, userB_id) VALUES (%s, %s)"
            cursor.execute(followSql, [userId, profileUserId, ])
    return HttpResponseRedirect("/timeline/" + profileUserId)

def search(request):
    userId = validateCookie(request)
    if not userId:
        return HttpResponseRedirect("/home")
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            queryString = request.POST.get('queryString')
            cursor = connection.cursor()
            searchUserSql = "SELECT name, userId FROM userModule_user WHERE name LIKE %s"
            cursor.execute(searchUserSql, [queryString + '%', ])
            searchResult = dictFetchAll(cursor)
            searchGroupSql = "SELECT groupName, groupId FROM groupModule_group WHERE groupName LIKE %s"
            cursor.execute(searchGroupSql, [queryString + '%', ])
            searchResult += dictFetchAll(cursor)

            return render(request, 'search.html', {'searchResult' : searchResult, 'userId' : userId, 'form' : form, })

    return render(request, 'search.html', {'form' : form, 'userId' : userId, })

# Check if the post with postId exists or not
def validPost(postId):
    cursor = connection.cursor()
    checkPostSql = "SELECT 1 FROM userModule_post WHERE postId=%s"
    cursor.execute(checkPostSql, [postId, ])
    isValidPost = cursor.fetchone()
    if isValidPost:
        return True
    return False

def like(request, postId):
    userId = validateCookie(request)
    if not userId:
        return HttpResponseRedirect('/home')
    cursor = connection.cursor()

    if not validPost(postId):
        return HttpResponseRedirect("/notfound")

    # Check if the user has already liked the posts or not
    checkUserSql = "SELECT 1 FROM userModule_like WHERE userId_id=%s AND postId_id=%s"
    cursor.execute(checkUserSql, [userId, postId, ])
    isLiked = cursor.fetchone()
    if isLiked:      # Already liked post
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Increment like value in Post table
    likeIncrementSql = "UPDATE userModule_post SET likes=likes+1 WHERE postId=%s"
    cursor.execute(likeIncrementSql, [postId, ])

    # Create a tuple in Like table
    addLikeSql = "INSERT INTO userModule_like (userId_id, postId_id) VALUES (%s, %s)"
    cursor.execute(addLikeSql, [userId, postId, ])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def getLike(request, postId):
    userId = validateCookie(request)
    if not userId:
        return HttpResponseRedirect('/home')
    cursor = connection.cursor()

    if not validPost(postId):
        return HttpResponseRedirect("/notfound")

    usersLikedSql = "SELECT userId, name FROM userModule_like RIGHT JOIN userModule_user ON userId_id=userId where postId_id=%s"
    cursor.execute(usersLikedSql, [postId, ])
    users = dictFetchAll(cursor)
    return render(request, 'getusers.html', {'users' : users, })

def comment(request, postId):
    userId = validateCookie(request)
    if not userId:
        return HttpResponseRedirect('/home')

    if not validPost(postId):
        return HttpResponseRedirect("/notfound")

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = request.POST.get('content')
            cursor = connection.cursor()
            # Increment comment value in Post table
            commentIncrementSql = "UPDATE userModule_post SET comments=comments+1 WHERE postId=%s"
            cursor.execute(commentIncrementSql, [postId, ])

            # Create a tuple in Comment table
            addCommentSql = "INSERT INTO userModule_comment (userId_id, postId_id, content) VALUES (%s, %s, %s)"
            cursor.execute(addCommentSql, [userId, postId, content, ])
            return HttpResponseRedirect("/newsfeed")

    return render(request, 'comment.html', {'form' : form, })

def getComment(request, postId):
    userId = validateCookie(request)
    if not userId:
        return HttpResponseRedirect('/home')
    cursor = connection.cursor()

    if not validPost(postId):
        return HttpResponseRedirect("/notfound")

    usersCommentsSql = "SELECT userId, name, content FROM userModule_comment RIGHT JOIN userModule_user\
                        ON userId_id=userId where postId_id=%s"
    cursor.execute(usersCommentsSql, [postId, ])
    users = dictFetchAll(cursor)
    return render(request, 'getusers.html', {'users' : users, })


def friends(request):
    userId = validateCookie(request)
    if not userId:
        return HttpResponseRedirect('/home')
    cursor = connection.cursor()

    # Fetch all the pending friend requests.
    getRequestsSql = "SELECT u.userId, name from userModule_user as u JOIN\
                     (SELECT userA_id as userId from userModule_friendship WHERE userB_id=%s AND status='R') as friends\
                     ON friends.userId=u.userId"
    cursor.execute(getRequestsSql, [userId, ])
    friendRequests = dictFetchAll(cursor)

    # Fetch all the userId and name of friends which have accepted friend requests
    getFriendsSql = "SELECT u.userId as userId, name from userModule_user as u JOIN\
                     (SELECT userA_id as userId from userModule_friendship WHERE userB_id=%s AND status='A'\
                     UNION\
                     SELECT userB_id as userId from userModule_friendship WHERE userA_id=%s AND status='A') as friends\
                     ON friends.userId=u.userId"
    cursor.execute(getFriendsSql, [userId , userId, ])
    friendsList = dictFetchAll(cursor)
    friendsCount = len(friendsList)

    return render(request, 'friends.html', {'friendsList' : friendsList, 'userId' : userId,\
                                            'friendRequests' : friendRequests, 'friendsCount' : friendsCount, })

def notfound(request):
    return render(request,'notfound.html')
