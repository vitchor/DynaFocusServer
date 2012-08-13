from django.conf.urls import patterns, include, url
from server.views import home

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from mysite.hello_file import hello_view
And then use:

('^test/$',hello_view)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', home),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
