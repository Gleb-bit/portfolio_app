from django.shortcuts import render
from django.views import generic

from blog.forms import CommentForm
from blog.models import Post, Comment


class BlogIndexView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog_index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-created_on')
        return queryset


class BlogCategoryView(generic.View):

    def get(self, request, category):
        posts = Post.objects.filter(categories__name__contains=category).order_by('-created_on')
        context = {
            "category": category,
            "posts": posts
        }
        return render(request, "blog_category.html", context)


class BlogDetailView(generic.DetailView):

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        form = CommentForm()
        context = {
            "post": post,
            'comments': comments,
            'form': form,
        }
        return render(request, "blog_detail.html", context)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data['author'],
                body=form.cleaned_data['body'],
                post=post
            )
            comment.save()
        context = {'post': post, 'comments': comments, 'form': form}
        return render(request, "blog_detail.html", context)
