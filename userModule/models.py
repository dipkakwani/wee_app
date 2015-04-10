from django.db import models
import os

def getImagePath(instance, filename):
    return os.path.join('static/userModule/images', str(instance.userid), filename)
    
def defaultImage():
    return os.path.join('static/userModule/images', 'default.png')

class User(models.Model):
    userid = models.AutoField(primary_key=True)

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
