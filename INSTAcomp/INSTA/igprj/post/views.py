from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from post.models import Tag, Stream, Follow, Post, Likes
from post.forms import NewPostForm
from django.urls import reverse
from userauths.models import Profile

from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(
        id__in=group_ids).all().order_by('-posted')
    context = {
        'post_items': post_items
    }

    return render(request, 'index.html', context)


def NewPost(request):
    user = request.user.id
    tags_objs = []

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tag')
            tags_list = list(tag_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p, created = Post.objects.get_or_create(
                picture=picture, caption=caption, user_id=user)
            p.tag.set(tags_objs)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()
    context = {
        'form': form
    }
    return render(request, 'new_post.html', context)


@login_required
def toggle_like(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Verificar si el usuario ya ha dado like
    user_has_liked = Likes.objects.filter(
        user=request.user, post=post_id).exists()
    print(user_has_liked)

    if user_has_liked:
        Likes.objects.filter(user=request.user, post=post).delete()
        post.likes += 1
    else:
        Likes.objects.create(user=request.user, post=post)
        post.likes -= 1

    # Guardar los cambios en el modelo Post
    post.save()
    return JsonResponse({
        'likes_count': post.likes,
        'user_has_liked': user_has_liked
    })


def favorite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    user_has_saved = profile.favorite.filter(id=post_id).exists()
    if user_has_saved:
        profile.favorite.remove(post)
    else:
        profile.favorite.add(post)

    return JsonResponse({
        'user_has_saved': user_has_saved,
    })
