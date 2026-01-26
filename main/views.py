from django.shortcuts import render
from posts.models import Post

def home(request):
    # Pobieramy najnowsze posty z publicznych blogów
    # Sortujemy od najnowszego (-created_at) i bierzemy tylko 6 pierwszych
    posts = Post.objects.filter(
        blog__is_public=True
    ).order_by('-created_at')[:6]

    return render(request, 'main/index.html', {
        'posts': posts
    })