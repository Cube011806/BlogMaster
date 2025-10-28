from django.shortcuts import render
from blogs.models import Blog

# Create your views here.
def dashboard(request):
    user_blogs = None
    if request.user.is_authenticated:
        user_blogs = Blog.objects.filter(owner=request.user).count()
    return render(request, 'stats/dashboard.html', {'user_blogs': user_blogs})