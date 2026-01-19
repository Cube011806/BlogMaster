from django.shortcuts import render
from posts.models import Post
import random

def home(request):
    # Pobieramy najnowsze posty z publicznych blogów
    posts = Post.objects.filter(
        blog__is_public=True
    ).order_by('-created_at')[:20]  # np. 20 najnowszych

    # Losujemy kolejność
    posts = list(posts)
    random.shuffle(posts)

    # Ograniczamy do np. 6 wyświetlanych
    posts = posts[:6]

    return render(request, 'main/index.html', {
        'posts': posts
    })
