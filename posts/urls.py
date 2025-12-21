from django.urls import path
from .views import post_list
from .views import post_detail
from .views import post_create
from .views import post_like

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:pk>/', post_detail, name='post_detail'),
    path('create/<int:blog_pk>/', post_create, name='post_create'),
    path('<int:pk>/like/', post_like, name='post_like'),
]
