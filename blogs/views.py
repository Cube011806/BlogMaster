from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Blog
from .forms import PostForm, BlogForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def blog_list(request):
    blogs = Blog.objects.order_by('-created_at')
    return render(request, 'blogs/blog_list.html', {'blogs': blogs})

@login_required
def user_blogs(request):
    blogs = request.user.blogs.all()  # używamy related_name='blogs' z modelu Blog
    return render(request, 'blogs/user_blogs.html', {'blogs': blogs})

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = request.user
            blog.save()
            return redirect('user_blogs')
    else:
        form = BlogForm()
    return render(request, 'blogs/blog_create.html', {'form': form})

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

@login_required
def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk, owner=request.user)  # tylko właściciel może edytować
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('user_blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blogs/blog_create.html', {'form': form})  # możesz użyć tego samego szablonu

@login_required
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk, owner=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('user_blogs')
    return render(request, 'blogs/blog_confirm_delete.html', {'blog': blog})
