from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<page>[0-9]+)/$', views.imageListView, name='imageList'),
]