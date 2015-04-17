from django.http import HttpResponse
from userModule.models import User
from userModule.models import Post
from userModule.models import Friendship
from userModule.models import Following
from userModule.models import Share
from userModule.models import Like
from userModule.models import Comment
from groupModule.models import Group
from groupModule.models import Join

def newsfeed(request):
    #TODO: Fetch the posts from currently logged in user's network.
    pass 

def timeline(request):
    #TODO: Fetch the posts of currently logged in user.
    pass

#This view lets the user post something.
def post(request):
    #TODO: Complete this view.
    pass

