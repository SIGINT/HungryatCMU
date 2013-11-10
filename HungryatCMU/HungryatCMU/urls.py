from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^', include('HungryApp.urls')),
    url(r'^HungryApp/', include('HungryApp.urls')),
)
