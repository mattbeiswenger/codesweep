from django.conf.urls import url
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.assignments, name='assignments'),
    url(r'^submit/$', views.submit_text, name='submit_text'),
    url(r'^find-assignments/$', views.find_assignments, name='find_assignments'),
    url(r'^(?P<assignment_name_slug>[\w\-]+)/$',
        views.show_assignment, name='show_assignment'),

]
