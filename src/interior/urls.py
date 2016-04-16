"""interior URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from interior_app.views import (PortfolioObjectList, 
                                ArticlesList, 
                                ArticleDetail)

urlpatterns = [
    url(r'^$', 'interior_app.views.home', name='home'),
    url(r'^subscribe/$', 'interior_app.views.subscribe', name='subscribe'),
    url(r'^portfolio/$', PortfolioObjectList.as_view(), name='portfolio'),
    url(r'^portfolio/bysort/$', 'interior_app.views.select_by_sort', name='select_by_sort'),
    url(r'^portfolio/(?P<object_id>\d+)/$', 'interior_app.views.portfolio_detail', name='portfolio_detail'),
    url(r'^services/$', 'interior_app.views.services', name='services'),
    url(r'^contacts/$', 'interior_app.views.contacts', name='contacts'),
    url(r'^blog/$', ArticlesList.as_view(), name='blog'),
    url(r'^blog/(?P<pk>\d+)/$', ArticleDetail.as_view(), name='article_detail'),
    url(r'^search/$', 'interior_app.views.search', name='search'),
    url(r'^category/(?P<id>\d+)/$', 'interior_app.views.category', name='category'),
    url(r'^tag/(?P<id>\d+)/$', 'interior_app.views.tag', name='tag'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
