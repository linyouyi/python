from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.login),
    url('^login/$', views.login),
    url('^logout/$', views.logout),
    url('^index/$', views.index),
    url('^user/repass/$', views.changePass),
    url('^host/$', views.hostList, name="host_list"),
    url('^host/group/$', views.hostGroup, name="host_group"),
    url('^host/group/add/$', views.hostGroupAdd),
    url('^host/group/edit/$', views.hostGroupEdit),
    url('^host/group/del/(\d+)/$', views.hostGroupDel),
    url('^host/list/$', views.hostList),
    url('^host/add/$', views.hostAdd),
    url('^host/edit/(\d+)/$', views.hostEdit),
    url('^host/del/(\d+)/$', views.hostDelete),
    url('^host/execute/$', views.hostExecute),
    url('^host/pi/$', views.hostPi),
    url('^host/monitor/$', views.hostMonitor),
    url('^host/upload/$', views.hostUpload),
    url('^host/search/$', views.hostSearch),

]