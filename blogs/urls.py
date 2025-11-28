from django.urls import path
from . import views
from .views import user_blogs

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('user/', user_blogs, name='user_blogs'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
]
