"""urlybird URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from bookmark import views as bookmark_views
from click import views as click_views
from api import views as api_views
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"bookmarks", api_views.BookmarkViewSet, base_name='bookmark')
# router.register(r'users', api_views.UserViewSet)
# router.register(r"^api/clicks", api_views.ClickViewSet)



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
    url('^register/', CreateView.as_view(
            template_name='bookmark/register.html',
            form_class=UserCreationForm,
            success_url='/index/'), name= "user_register"),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', bookmark_views.user_logout, name="logout"),
    url(r'^index/', TemplateView.as_view(template_name="bookmark/index.html")),
    url(r'bookmark/add/$',bookmark_views.BookmarkCreate.as_view(), name='bookmark_add'),
    url(r'bookmark/(?P<pk>[0-9]+)/update/$', bookmark_views.BookmarkUpdate.as_view(), name='bookmark_update'),
    url(r'bookmark/(?P<pk>[0-9]+)/delete/$', bookmark_views.BookmarkDelete.as_view(), name='bookmark_delete'),
    url(r'^bookmark/allbookmarks', bookmark_views.BookmarkList.as_view(), name='bookmark_list'),
    url(r'^bookmark/user_bookmarks/(?P<user_id>[0-9]+)/$', bookmark_views.UserBookmarkList.as_view(), name='user_bookmarks'),
    url(r'b/(?P<short_id>[A-Za-z0-9]+)/$', click_views.click_tracker, name='click_tracker'),
    url(r'bookmark/display/(?P<pk>[0-9]+)/$', bookmark_views.bookmark_display, name='bookmark_display'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace ='rest_framework')),
    url(r'^api/clicks/$', api_views.ClickCreateView.as_view()), #needs a bookmark-detail
    # url(r'^api/bookmarks/(?P<pk>\d+)$', api_views.BookmarkViewSet, name='bookmark-detail'),
    url(r'^api/bookmarks/click/(?P<pk>\d+)$', api_views.ClickDetailView.as_view(), name='click-detail'),
    url(r'^api/bookmarks/(?P<pk>\d+)/clickset$', api_views.ClickList.as_view(), name='click-list'),
    url(r'^api/userset/$', api_views.UserList.as_view(), name='user-list'),
    url(r'^api/users/(?P<pk>\d+)$', api_views.UserDetailView.as_view(), name='user-detail'),
    url(r'^api/user/$', api_views.UserCreateView.as_view(), name='user-create'),
]

