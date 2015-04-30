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
    postsSql = "SELECT * FROM userModule_post g1\
                WHERE (SELECT g2.groupId_id FROM groupModule_joins g2 WHERE g1.groupId_id = g2.groupId_id AND userId_id=%s AND status='A')\
                UNION\
                SELECT * FROM userModule_post u1\
                WHERE\
                    (SELECT userB_id FROM userModule_following WHERE userA_id=%s AND userB_id=u1.posterId_id\
                    UNION\
                    SELECT userA_id FROM userModule_friendship WHERE userB_id=%s AND status='A' AND userA_id=u1.posterId_id\
                    UNION\
                    SELECT userB_id FROM userModule_friendship WHERE userA_id=%s AND status='A' AND userB_id=u1.posterId_id\
                    UNION\
                    SELECT %s as userId FROM userModule_user where u1.posterId_id=%s LIMIT 1)\
                ORDER BY time desc;"
    cursor = connection.cursor()
    cursor.execute(postsSql, [userId, ] * 6)
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

        # Check if the user is friend (including pending friend request) or not.
        friendSql = "SELECT 1 FROM userModule_friendship WHERE userA_id=%s AND userB_id=%s OR\
                     userA_id=%s AND userB_id=%s"
        cursor.execute(friendSql, [userId, profileUserId, profileUserId, userId, ])
        isFriend = cursor.fetchall()

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
                'isSelf' : isSelf, 'len' : len(posts), 'userId': userId, 'user' : user, })
     
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
def updateFriend(request, profileUserId):
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
            for result in searchResult:
                if 'userId' in result:
                    result['link'] = "/timeline/" + str(result['userId'])
                else:
                    result['link'] = "/group/" + str(result['groupId'])
            return render(request, 'search.html', {'searchResult' : searchResult, 'userId' : userId, 'form' : form, })

    return render(request, 'search.html', {'form' : form, 'userId' : userId, })

def notfound(request):
    return render(request,'notfound.html')
