
from django.shortcuts import render
from blogs.models import *
from blogs.paginator import *


def blog_index(request):
    # here we expect page from UI for pagination
    page = request.get('page', None)
    posts = Post.objects.all().order_by("-created_on")
    if page:
        posts = pagination(page, posts)
    context = {
        "posts": posts,
    }
    return render(request, "blogs/index.html", context)


def blog_category(request, category):
    page = request.get('page', None)
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    if page:
        posts = pagination(page, posts)
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blogs/category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    page = request.get('page', None)
    comments = Comment.objects.filter(post=post)
    if page:
        comments = pagination(page, comments)
    context = {
        "post": post,
        "comments": comments,
    }

    return render(request, "blogs/detail.html", context)


def pagination(page, queryset, no_of_rows=25):
    if page is not None:
        paginator = Paginator(queryset, no_of_rows)
        try:
            data = paginator.page(int(page))
        except PageNotAnInteger:
            data = []
            pass
        except InvalidPage:
            data = []
            pass
        return data
    return queryset
