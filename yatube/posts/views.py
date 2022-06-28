from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User
from .utils import paginator_func


def index(request):
    posts_list = Post.objects.select_related('author').all()
    page_obj = paginator_func(request, posts_list)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.select_related('group').all()
    page_obj = paginator_func(request, posts_list)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = author.posts.select_related('author').filter(author=author)
    page_obj = paginator_func(request, author_posts)
    context = {
        'author': author,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid() is False or request.method == 'GET':
        return render(request, 'posts/create_post.html', {'form': form})
    post = form.save(False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', username=request.user.username)


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid() is False or request.method == 'GET':
            return render(request, 'posts/create_post.html', {'form': form})
        form.save()
    return redirect('posts:post_detail', post_id=post.pk)
