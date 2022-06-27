from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm

from .models import Group, Post, User


def index(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.all()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author_username = get_object_or_404(User, username=username)
    author_posts = Post.objects.filter(author=author_username)
    paginator = Paginator(author_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'name': author_username,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    post_count = Post.objects.filter(author=post.author).count()
    text = post.text[:30]
    context = {
        'post': post,
        'text': text,
        'post_count': post_count
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            post = form.save(False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user.username)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    groups = Group.objects.all()
    return render(
        request,
        'posts/create_post.html',
        {
            'form': form,
            'groups': groups
        }
    )


def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    groups = Group.objects.all()
    is_edit = True
    if request.user.id == post.author_id:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            updated_data = form.save(False)
            updated_data.author = request.user
            updated_data.save()
            post.text = text
            post.group = group
            post.save()
            return redirect('posts:post_detail', post_id=post.id)
        return render(
            request,
            'posts/create_post.html',
            {
                'form': form,
                'groups': groups,
                'is_edit': is_edit,
                'post': post
            }
        )
    return redirect('posts:post_detail', post_id=post.pk)
