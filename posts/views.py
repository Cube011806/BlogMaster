from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from blogs.models import Blog
from comments.forms import CommentForm

def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    top_level_comments = post.comments.filter(parent__isnull=True)

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comment_form': CommentForm(),
        'top_level_comments': top_level_comments
    })

@login_required
def post_create(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk, owner=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.blog = blog
            post.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form, 'blog': blog})

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "count": post.likes.count()
    })
