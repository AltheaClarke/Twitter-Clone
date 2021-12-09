from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy, reverse
from cloudinary.forms import cl_init_js_callbacks


def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Yes,Save
            form.save()
        # Redirect to home
            return HttpResponseRedirect('/')
        else:
            # No, show error
            return HttpResponseRedirect(form.errors.as_json())

    # Get all posts,limit = 20
    posts = Post.objects.all().order_by('-created_at')[:20]

    # Show
    return render(request, 'posts.html',
                  {'posts': posts})


def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect("/")


def like(request, post_id):
    newlikecount = Post.objects.get(id=post_id)
    newlikecount.likecount += 1
    newlikecount.save()
    return HttpResponseRedirect("/")


def edit(request, post_id):
    posts = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=posts)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect("not valid")
    form = PostForm
    return render(request, "edit.html", {"posts": posts})
