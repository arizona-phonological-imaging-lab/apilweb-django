from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<page>[0-9]+)/$', views.imageListView, name='imageList'),
    url(r'^tag/$', views.tagView, name='tag'),
    url(r'^untag/$', views.untagView, name='untag'),
    url(r'^get-all-ids/$', views.getAllIDsView, name='getallids'),
    url(r'^download/$', views.downloadView, name='download'),
    url(r'^addexp/$', views.addexpView, name='addexp'),
    url(r'^removeexp/$', views.removeexpView, name='removeexp'),
    url(r'^handle-search/(?P<page>[0-9]+)/$', views.searchHandlerView, name='searchHandler'),
    url(r'^addfiles/$', views.addFilesView, name='addFiles'),
    url(r'^successfullyadded/$', views.addsuccess, name='addFiles'),
]