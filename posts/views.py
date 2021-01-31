from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Post, Group
from .forms import PostForm
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_post_list = group.posts.all()
    paginator = Paginator(group_post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(request, 'group.html', {'group': group, 'page': page})


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'new_post.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    form.save()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_post_list = author.posts.all()
    author_post_count = author.posts.count()
    paginator = Paginator(author_post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(request, 'profile.html', {'page': page})
 

def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=username)
    author_post_count = author.posts.count()
    return render(request, 'post.html', {'post': post, 'author_post_count': author_post_count})

@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=username)
    if request.user != author:
        return redirect('post', username=author.username, post_id=post.id)
    form =PostForm(request.Post or None, instance=post)
    if form.is_valid():
        post.save()
        return redirect('post', username=author.username, post_id=post.id)
    return render(request, 'new_post.html', {{'form':form, 'post': post}}) 