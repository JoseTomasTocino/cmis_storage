from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get/(?P<path>.+)$', views.get_file,  name='cmis_storage_get_file'),
]
