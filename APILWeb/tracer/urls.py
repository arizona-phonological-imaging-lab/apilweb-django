from django.conf.urls import url
from . import views

#@app.route('/draw', methods = ['GET', 'POST'])
urlpatterns = [
    url(r'^draw/$', views.trace, name='trace'),
]
