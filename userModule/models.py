"""
Author : Diptanshu Kakwani
Contains all the models that are realted to users.
"""
from django.db import models
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

#TODO: Add all user related tables.
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
    STATUS = (('F', 'Following'),)
    status = models.CharField(max_length=1, choices=STATUS)
    class Meta:
        unique_together = (("userA"), ("userB"),)
