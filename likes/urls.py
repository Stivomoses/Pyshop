from django.urls import path
from . import views

app_name = 'likes'
urlpatterns = [
    path('', views.index, name='index'),
    path('liked_brands', views.liked_brands, name='liked_brands'),
    path('updatelike', views.update_like, name='update_like')
]
