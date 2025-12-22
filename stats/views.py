from django.shortcuts import render
from blogs.models import Blog
from posts.models import Post, PostVisit
from comments.models import Comment

def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, "stats/dashboard.html", {})

    user = request.user

    # Blogi użytkownika
    blogs = Blog.objects.filter(owner=user)
    blogs_count = blogs.count()

    # Posty użytkownika
    posts = Post.objects.filter(blog__owner=user)
    posts_count = posts.count()

    # Komentarze pod jego postami (bez jego własnych)
    comments_count = Comment.objects.filter(
        post__in=posts
    ).exclude(author=user).count()

    # Polubienia jego postów (bez jego własnych)
    post_likes = sum(
        post.likes.exclude(id=user.id).count()
        for post in posts
    )

    # Odwiedziny jego postów (bez jego własnych)
    visits_count = PostVisit.objects.filter(
        post__in=posts
    ).exclude(user=user).count()

    return render(request, 'stats/dashboard.html', {
        'blogs_count': blogs_count,
        'posts_count': posts_count,
        'comments_count': comments_count,
        'post_likes': post_likes,
        'visits_count': visits_count,
    })

