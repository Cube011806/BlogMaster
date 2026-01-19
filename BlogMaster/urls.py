from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('blogs/', include('blogs.urls')),
    path('posts/', include('posts.urls')),
    path('comments/', include('comments.urls')),
    path('stats/', include('stats.urls')),

    # CKEditor upload
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
