from django.urls import path
from .views import add_comment

urlpatterns = [
    path('add/<int:post_pk>/', add_comment, name='add_comment'),
]
