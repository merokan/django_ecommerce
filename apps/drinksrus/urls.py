from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^admin_login$', views.admin_login),
    url(r'^home/(?P<pagenum>\d+)$', views.home),
    url(r'^product/(?P<prodnum>\d+)$', views.home),
    url(r'^logout$', views.logout),
    url(r'^search$',views.search),
    url(r'^admin_dashboard$',views.admindashboard),
]