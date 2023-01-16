from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('review/<pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='detail_review'),
    path('review/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review'),

    path('countries/image/<pk>/', CountryImageView.as_view(), name='country_image'),
    path('countries/plus/reload/', ContriesReloadView.as_view(), name='reload_countries'),
    path('countries/plus/find/', ContriesFindView.as_view(), name='find_countries'),
    path('countries/<pk>/', CountryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='detail_country'),
    path('countries/', CountryViewSet.as_view({'get': 'list', 'post': 'create'}), name='country'),

    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
