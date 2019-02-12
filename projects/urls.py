from django.conf.urls import url
from projects.views import LoginPage, LoginAPIView, DashBoard, ProjectView, ProjectAPIView, DashboardAPIView

urlpatterns = [
        url(r'^$', LoginPage.as_view(),name='login'),
        url(r'^dashboard_api/$', DashboardAPIView.as_view(),name='dashboard_api'),
        url(r'^login_check/$', LoginAPIView.as_view(),name='login_check'),
        url(r'^project_api/$', ProjectAPIView.as_view(),name='project_api'),
        url(r'^dashboard/$', DashBoard.as_view(),name='dashboard'),
        url(r'^project/(?P<pk>[0-9]+)/$', ProjectView.as_view(),name='project'),

]
