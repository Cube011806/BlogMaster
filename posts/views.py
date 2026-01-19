from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, PostVisit
from .forms import PostForm
from blogs.models import Blog
from comments.forms import CommentForm
from django.http import JsonResponse



def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Zapis odwiedzin posta
    PostVisit.objects.create(
        post=post,
        user=request.user if request.user.is_authenticated else None,
        ip=request.META.get("REMOTE_ADDR")
    )

    # Poprzedni post (największy ID mniejszy niż obecny)
    previous_post = Post.objects.filter(id__lt=post.id).order_by('-id').first()

    # Następny post (najmniejszy ID większy niż obecny)
    next_post = Post.objects.filter(id__gt=post.id).order_by('id').first()

    # Poprzedni post (największy ID mniejszy niż obecny)
    previous_post = Post.objects.filter(
    blog=post.blog,
    id__lt=post.id
    ).order_by('-id').first()

    # Następny post (najmniejszy ID większy niż obecny)
    next_post = Post.objects.filter(
        blog=post.blog,
        id__gt=post.id
    ).order_by('id').first()


    top_level_comments = post.comments.filter(parent__isnull=True)

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comment_form': CommentForm(),
        'top_level_comments': top_level_comments,
        'previous_post': previous_post,
        'next_post': next_post,
    })



@login_required
def post_create(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # DODANO request.FILES
        if form.is_valid():
            post = form.save(commit=False)
            post.blog = blog
            post.author = request.user
            post.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = PostForm()

    return render(request, 'posts/post_form.html', {
        'form': form,
        'blog': blog,
        'is_edit': False,
    })


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # DODANO request.FILES
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=post.blog.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_form.html', {
        'form': form,
        'blog': post.blog,
        'is_edit': True,
    })



@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_detail', pk=post.blog.pk)
    return render(request, 'posts/post_confirm_delete.html', {'post': post})



@login_required
def post_like(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Musisz być zalogowany, aby polubić post!'}, status=403)

    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})
