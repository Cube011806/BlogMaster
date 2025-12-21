from django.urls import path
from .views import add_comment
from .views import like_comment


urlpatterns = [
    path('add/<int:post_pk>/', add_comment, name='add_comment'),
    path('<int:pk>/like/', like_comment, name='like_comment'),
]
