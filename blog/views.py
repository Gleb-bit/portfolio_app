from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from blog.forms import CommentForm, ExtendedRegisterForm, AccountForm, BlogDocumentForm
from blog.models import Post, Comment, Profile, Category


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
            author = self.check_user_authenticated(request, form)
            comment = Comment(
                author=author,
                body=form.cleaned_data['body'],
                post=post,
                user=request.user if isinstance(request.user, User) else None
            )
            comment.save()
        context = {'post': post, 'comments': comments, 'form': form}
        return render(request, "blog_detail.html", context)

    def check_user_authenticated(self, request, form):
        if request.user.is_authenticated:
            author = request.user.profile.name
        elif form.cleaned_data['author']:
            author = form.cleaned_data['author']
        else:
            author = 'Anonim'
        return author


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'create_post.html'
    form_class = BlogDocumentForm

    def post(self, request, *args, **kwargs):
        blog_form = BlogDocumentForm(request.POST)
        if blog_form.is_valid():
            categories = Category.objects.create(name=blog_form.cleaned_data['categories'])
            title = blog_form.cleaned_data.get('title')
            body = blog_form.cleaned_data.get('body')
            user = request.user.profile
            instance = Post.objects.create(title=title, body=body, user=user)
            instance.categories.set([categories])
            return HttpResponseRedirect('/blog/')
        return render(request, 'create_post.html', context={'form': blog_form})


class DetailAccountView(generic.DetailView):
    model = Profile
    context_object_name = 'profile_list'
    template_name = 'detail_account.html'


class EditAccountView(generic.UpdateView):
    redirect_field_name = 'main/'
    form_class = AccountForm
    model = Profile
    template_name = 'edit_account.html'
    context_object_name = 'account_form'
    pk_url_kwarg = 'pk'
    success_url = '/blog/'


class RegisterView(generic.View):

    def get(self, request, *args, **kwargs):
        form = ExtendedRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = ExtendedRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.errors)
            user = form.save()
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            about_me = form.cleaned_data.get('about_me')
            avatar = form.cleaned_data.get('avatar')
            Profile.objects.create(user=user, name=name, surname=surname, about_me=about_me, avatar=avatar)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/blog')
        else:
            form = ExtendedRegisterForm()
        return render(request, 'register.html', {'form': form})


class OurLoginView(LoginView):
    template_name = 'login.html'


class OurLogoutView(LogoutView):
    template_name = 'logout.html'
