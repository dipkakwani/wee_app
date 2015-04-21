from django.conf.urls import patterns, include, url
from django.contrib import admin
from userModule.views import home
from userModule.views import logout
from wee.views import newPost

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wee.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', home),
    url(r'^logout/$', logout),
    url(r'^post/$', newPost),
)
