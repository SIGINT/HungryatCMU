from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'HungryApp.views.home', name='home'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'HungryApp/login.html'}),
    url(r'^Studentregister$', 'HungryApp.views.StudentRegistration'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^forgotpassword$','HungryApp.views.forgotpassword'),
    url(r'^resetpassword$','HungryApp.views.resetpassword'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'HungryApp.views.confirm_registration', name='confirm'),
)





