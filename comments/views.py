from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import Comment
from posts.models import Post
from django.http import JsonResponse
from django.template.loader import render_to_string

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

            parent_id = request.POST.get("parent_id")
            if parent_id:
                comment.parent = Comment.objects.get(pk=parent_id)

            comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string("comments/comment.html", {
                    "comment": comment,
                    "post": post,
                    "user": request.user
                })
                return JsonResponse({"html": html})

    return redirect('post_detail', pk=post.pk)