from django.conf.urls import patterns, include, url
from django.contrib import admin
from wee.views import hello
from userModule.views import home

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wee.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$', hello),
    url(r'^home/$', home),
)
