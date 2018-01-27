from django.conf.urls import url
from mainapp import views

urlpatterns = [
    url(r'^$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^submit/$', views.submit_text, name='submit_text'),
    url(r'^(?P<assignment_name_slug>[\w\-]+)/$',
        views.show_assignment, name='show_assignment')

]
