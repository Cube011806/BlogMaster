from django.shortcuts import redirect, get_object_or_404
from .forms import CommentForm
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('post_detail', pk=post.pk)