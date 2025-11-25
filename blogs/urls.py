from django.urls import path
from . import views
from .views import blog_list, post_detail, post_create, user_blogs

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('user/', user_blogs, name='user_blogs'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    #niby tutaj jest konflikt zmiana na blogs/create i posts/create?
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
]
