from django.shortcuts import render
from blogs.models import Blog
from posts.models import Post

# Create your views here.
def dashboard(request):
    blogs_count = 0
    posts_count = 0
    if request.user.is_authenticated:
        # policz blogi użytkownika
        blogs = Blog.objects.filter(owner=request.user)
        blogs_count = blogs.count()
        # policz posty we wszystkich blogach użytkownika
        posts_count = Post.objects.filter(blog__in=blogs).count()

    return render(request, 'stats/dashboard.html', {
        'blogs_count': blogs_count,
        'posts_count': posts_count
    })