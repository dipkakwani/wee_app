from django.conf.urls import patterns, include, url
from django.contrib import admin
from userModule.views import home
from userModule.views import logout
from groupModule.views import createGroup
from groupModule.views import group
from groupModule.views import groupSettings
from wee.views import newPost
from wee.views import timeline
from wee.views import newsfeed
from wee.views import friend
from wee.views import notfound

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wee.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', home),
    url(r'^logout/$', logout),
    url(r'^post/$', newPost),
    url(r'newgroup/', createGroup),
    url(r'^group/(?P<groupId>\d+)/$', group),
    url(r'^group/(?P<groupId>\d+)/settings$', groupSettings),
    url(r'^timeline/(?P<profileUserId>\d+)/friend.html', friend),
    url(r'^timeline/(?P<profileUserId>\d+)/$', timeline),
    url(r'^.*/$', notfound)
)
