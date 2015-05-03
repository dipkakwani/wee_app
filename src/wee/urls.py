from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from userModule.views import home
from userModule.views import userSettings
from userModule.views import logout
from groupModule.views import createGroup
from groupModule.views import group
from groupModule.views import selectgroup
from groupModule.views import groupSettings
from wee.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wee.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', home),
    url(r'^newsfeed/$', newsfeed),
    url(r'^logout/$', logout),
    url(r'^post/$', newPost),
    url(r'^newgroup/$', createGroup),
    url(r'^settings/$', userSettings),
    url(r'^group/(?P<groupId>\d+)/$', group),
    url(r'^groups/$' , selectgroup),
    url(r'^group/(?P<groupId>\d+)/settings/$', groupSettings),
    url(r'^friends/$' , friends) ,
    url(r'^timeline/(?P<profileUserId>\d+)/(?P<change>\w)/friend/$', updateFriend),
    url(r'^timeline/(?P<profileUserId>\d+)/follow/$', updateFollow),
    url(r'^timeline/(?P<profileUserId>\d+)/$', timeline),
    url(r'^search/$', search),
    url(r'^like/(?P<postId>\d+)/$', like),
    url(r'^getlike/(?P<postId>\d+)/$', getLike),
    url(r'^comment/(?P<postId>\d+)/$', comment),
    url(r'^getcomment/(?P<postId>\d+)/$', getComment),


)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += patterns('', url(r'^.*/$', notfound), )
