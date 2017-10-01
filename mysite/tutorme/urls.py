from django.conf.urls import url
from . import views as core_views 

urlpatterns = [
    url(r'^$', core_views.index),
    url(r'^signup/$', core_views.signup),
]
