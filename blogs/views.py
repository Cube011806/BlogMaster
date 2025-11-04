from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Blog
from .forms import PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'blogs/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blogs/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            blog = Blog.objects.filter(owner=request.user).first()
            if not blog:
                blog = Blog.objects.create(owner=request.user, title=f"Blog {request.user.email}")
            post.blog = blog
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blogs/post_form.html', {'form': form})