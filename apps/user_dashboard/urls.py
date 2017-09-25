from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.index),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^users/new$', views.create),
    url(r'^users/edit$', views.profile),
    url(r'^users/edit/(?P<id>\d+)$', views.edit),
    url(r'^users/show/(?P<id>\d+)$', views.show),
    url(r'^users/addmessage/(?P<id>\d+)$', views.addmessage),
    url(r'^users/addcomment/(?P<user_id>\d+)/(?P<mess_id>\d+)$', views.addcomment),
]
