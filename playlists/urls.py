
"""playlists URL Configuration

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
from django.conf.urls import url
from django.contrib import admin

import playlist.views as playlist_views

urlpatterns = [
    url(r'^mixd/$', playlist_views.list),
    url(r'^mixd/admin/', admin.site.urls),
    url(r'^mixd/auth', playlist_views.auth),
    url(r'^mixd/list', playlist_views.list),
    url(r'^mixd/playlist_detail', playlist_views.detail),
    url(r'^mixd/add', playlist_views.add),
    url(r'^mixd/save', playlist_views.save),
    url(r'^mixd/search', playlist_views.search),
    url(r'^mixd/share', playlist_views.share),
    # Development only junk, get rid of these when the app is fully functional.
    url(r'^mixd/playlistseedtags$', playlist_views.seedTags),
]
