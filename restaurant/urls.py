"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app.views import (IndexView, CreateUserView, ProfileUpdateView, MenuItemCreateView,
MenuItemListView, MenuItemUpdateView, MenuItemDetailView, MenuItemDeleteView, OrderCreateView, OrderListView, OrderDetailView)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^create_user/$', CreateUserView.as_view(), name='create_user_view'),
    url(r'^accounts/profile/$', login_required(ProfileUpdateView.as_view()), name="profile_update_view"),
    url(r'^menu_item_create/$', login_required(MenuItemCreateView.as_view()), name='menu_item_create_view'),
    url(r'^menu_item_list/$', login_required(MenuItemListView.as_view()), name='menu_item_list_view'),
    url(r'^menu_item_detail/(?P<pk>\d+)/$', login_required(MenuItemDetailView.as_view()), name='menu_item_detail_view'),
    url(r'^update_menu_item/(?P<pk>\d+)/$', login_required(MenuItemUpdateView.as_view()), name='menu_item_update_view'),
    url(r'^delete_menu_item/(?P<pk>\d+)/$', login_required(MenuItemDeleteView.as_view()), name='menu_item_delete_view'),
    url(r'^order_create/$', login_required(OrderCreateView.as_view()), name='order_create_view'),
    url(r'^order_list', login_required(OrderListView.as_view()), name='order_list_view'),
    url(r'^order_detail/(?P<pk>\d+)/$', login_required(OrderDetailView.as_view()), name='order_detail_view'),


]
