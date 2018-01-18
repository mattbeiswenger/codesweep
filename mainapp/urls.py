from django.conf.urls import url
from mainapp import views

urlpatterns = [
    url(r'^$', views.hw, name='hw'),
    url(r'^(?P<assignment_name_slug>[\w\-]+)/$',
        views.show_assignment, name='show_assignment')
]
