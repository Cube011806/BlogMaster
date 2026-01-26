from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import CommentForm
from .models import Comment
from posts.models import Post

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

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': comment.likes.count()})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author or request.user == comment.post.author:
        comment.delete()
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'status': 'error'}, status=403)

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return JsonResponse({'status': 'error'}, status=403)
    if request.method == 'POST':
        new_text = request.POST.get('text')
        if new_text:
            comment.text = new_text
            comment.save()
            return JsonResponse({'status': 'updated', 'text': comment.text})
    return JsonResponse({'status': 'error'}, status=400)