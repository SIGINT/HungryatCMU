from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'hungry.views.home'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'hungry/login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
)