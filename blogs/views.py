from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def blog_list(request):
    blogs = Blog.objects.order_by('-created_at')
    return render(request, 'blogs/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    posts = blog.posts.order_by('-created_at')
    return render(request, 'blogs/blog_detail.html', {
        'blog': blog,
        'posts': posts,
    })

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
