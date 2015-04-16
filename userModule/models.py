"""
Author : Diptanshu Kakwani
Contains all the models that are related to users.
"""
from django.db import models
from datetime import datetime
import os

#Returns the path of the profile picture
def getImagePath(instance, filename):
    return os.path.join('static/userModule/images', str(instance.userid), filename)
    
#Returns the path of the default profile picture
def defaultImage():
    return os.path.join('static/userModule/images', 'default.png')

#Model storing the information of all the registered users.
class User(models.Model):
    userId = models.AutoField(primary_key=True)

    name = models.CharField(max_length=30)

    email = models.EmailField(max_length=40, unique=True)

    password = models.CharField(max_length=70)

    dob = models.DateField()

    SEX = (('M', 'Male'),('F', 'Female'),)
    sex = models.CharField(max_length=1, choices=SEX)

    description = models.CharField(max_length=160, blank=True, default="")

    profilePic = models.ImageField(upload_to=getImagePath, default=defaultImage)

    school = models.CharField(max_length=50, blank=True, default="")

    college = models.CharField(max_length=50, blank=True, default="")

    companyName = models.CharField(max_length=50, blank=True, default="")

    STATUS = (('S', 'Single'), ('M', 'Married'), ('', 'Unkown'),)
    status = models.CharField(max_length=1, choices=STATUS, blank=True, default="")

    profession = models.CharField(max_length=30, blank=True, default="")

    website = models.URLField(blank=True, default="")

#NOTE:Django doesn't support composite primary key, so create a single compound unique key with Meta.unique_together .

"""
A many-to-many relationship on User.
The order in which the user id appears determines which user has sent the friend request. 
This approach avoids storing two tuples per friendship.
"""
class Friendship(models.Model):
    userA = models.ForeignKey('User', related_name='Friendship.userA')
    userB = models.ForeignKey('User', related_name='Friendship.userB')
    STATUS = (('R', 'RequestSent'), ('F', 'Friends'),)
    status = models.CharField(max_length=1, choices=STATUS)
    class Meta:
        unique_together = (("userA"), ("userB"),)

#A many-to-many relationship on User.
class Following(models.Model):
    userA = models.ForeignKey('User', related_name='Following.userA')
    userB = models.ForeignKey('User', related_name='Following.userB')
    class Meta:
        unique_together = (("userA"), ("userB"),)
        
"""
A post may or may not belong to a Group.
"""
class Post(models.Model):
    postId = models.AutoField(primary_key=True)
    posterId = models.ForeignKey('User')
    PRIVACY = (('L','Limited'), ('P', 'Public'),)
    privacy = models.CharField(max_length=1, choices=PRIVACY)
    time = models.DateTimeField(default=datetime.now)
    likes = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)
    shares = models.BigIntegerField(default=0)
    content = models.TextField()
    groupId = models.ForeignKey('groupModule.Group', null=True)
    class Meta:
        ordering = ['-time']


class Share(models.Model):
    userId = models.ForeignKey('User', related_name='Share.userId')
    postId = models.ForeignKey('Post', related_name='Share.postId')
    class Meta:
        unique_together = (('userId'), ("postId"),)    

class Like(models.Model):
    userId = models.ForeignKey('User', related_name='Like.userId')
    postId = models.ForeignKey('Post', related_name='Like.postId')
    class Meta:
        unique_together = (('userId'), ("postId"),)    

class Comment(models.Model):
    userId = models.ForeignKey('User', related_name='Comment.userId')
    postId = models.ForeignKey('Post', related_name='Comment.postId')
    content = models.CharField(max_length=140)
    class Meta:
        unique_together = (('userId'), ("postId"),)
