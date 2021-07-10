import logging
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from blog.forms import CommentForm, ExtendedRegisterForm, AccountForm, PostDocumentForm
from blog.models import Post, Comment, Profile, Category

logger = logging.getLogger(__name__)


def get_now():
    return datetime.now()


class ListCategoryView(generic.ListView):

    def get(self, request, *args, **kwargs):
        category = kwargs['category']
        posts = Post.objects.filter(categories__name=category).order_by('-created')
        context = {
            "category": category,
            "posts": posts
        }
        return render(request, "list_category.html", context)


class ListPostView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'list_post.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-created')
        return queryset


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostDocumentForm

    def post(self, request, *args, **kwargs):

        blog_form = PostDocumentForm(request.POST, request.FILES)

        if blog_form.is_valid():
            title = blog_form.cleaned_data.get('title')
            body = blog_form.cleaned_data.get('body')
            profile = request.user.profile
            image = blog_form.cleaned_data.get('image')

            self.set_or_not_categories(blog_form, title=title, body=body, profile=profile, image=image)

            return HttpResponseRedirect('/blog/')

        return render(request, 'create_post.html', context={'form': blog_form})

    def set_or_not_categories(self, form, **kwargs):
        categories = []

        instance = Post.objects.create(title=kwargs['title'], body=kwargs['body'], profile=kwargs['profile'],
                                       image=kwargs['image'])

        if form.cleaned_data['categories']:

            for category in form.cleaned_data['categories'].split():
                categories.append(Category.objects.get_or_create(name=category)[0])

            instance.categories.set(categories)


class EditPostView(generic.UpdateView):
    queryset = Post.objects.all()
    form_class = PostDocumentForm
    template_name = 'edit_post.html'
    context_object_name = 'post'
    success_url = '/blog/'

    def form_valid(self, form):

        categories = [category for category in self.object.categories.all()]
        category_tokens = form.cleaned_data['categories'].split()
        current_categories_names = [category.name for category in self.object.categories.all()]
        categories_to_update = set(category_tokens) - set(current_categories_names)
        categories_to_delete = set(current_categories_names) - set(category_tokens)

        if categories_to_update:
            categories = self.get_categories_to_update(categories_to_update)

        if categories_to_delete:
            categories = self.get_categories_to_delete(categories_to_delete)

        profile = self.request.user.profile
        title = form.cleaned_data.get('title')
        body = form.cleaned_data.get('body')
        image = form.cleaned_data.get('image')

        Post.objects.filter(pk=self.object.pk).delete()

        instance = Post.objects.create(id=self.object.pk, title=title, body=body, profile=profile, image=image)

        instance.categories.set(categories)

        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        object = self.get_object()

        post_categories = object.categories.all()
        categories = ' '.join(category.name for category in post_categories)

        form_data = {
            'title': object.title,
            'body': object.body,
            'image': object.image,
            'categories': categories
        }
        form = PostDocumentForm(initial=form_data)

        return render(request, self.template_name, {'form': form, 'post': object})

    def get_success_url(self):
        post = self.object
        return f'/blog/{post.pk}/'

    def get_categories_to_update(self, edit_categories):
        categories = [category for category in self.object.categories.all()]

        for category in edit_categories:
            categories.append(Category.objects.get_or_create(name=category)[0])

        return categories

    def get_categories_to_delete(self, edit_categories):
        categories = [category for category in self.object.categories.all() if category.name not in edit_categories]

        for category in edit_categories:
            Category.objects.filter(name=category).delete()

        return categories


class DeletePostView(generic.DeleteView):
    model = Post
    template_name = 'delete_post_confirm.html'
    success_url = '/blog/'


class DetailPostView(generic.DetailView):

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
        return render(request, "detail_post.html", context)

    def post(self, request, pk):

        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            author = self.get_author_name(request, form)

            comment = Comment(
                author=author,
                body=form.cleaned_data['body'],
                image=form.cleaned_data['image'] if 'image' in form.cleaned_data else None,
                post=post,
                user=request.user if isinstance(request.user, User) else None
            )
            comment.save()

        context = {'post': post, 'comments': comments, 'form': form}
        return render(request, "detail_post.html", context)

    def get_author_name(self, request, form):
        if request.user.is_authenticated:
            author = request.user.profile.name
        elif form.cleaned_data['author']:
            author = form.cleaned_data['author']
        else:
            author = 'Anonim'
        return author


class EditCommentView(generic.UpdateView):
    form_class = CommentForm
    model = Comment
    template_name = 'edit_comment.html'

    def get_success_url(self):
        queryset = super().get_queryset()
        current_comment = queryset.filter(pk=self.object.pk)[0]
        post = Post.objects.only('pk').filter(id=current_comment.post_id)[0]
        return f'/blog/{post.pk}/'


class DeleteCommentView(generic.DeleteView):
    model = Comment
    template_name = 'delete_comment_confirm.html'

    def get_success_url(self):
        queryset = super().get_queryset()
        current_comment = queryset.filter(pk=self.object.pk)[0]
        post = Post.objects.only('pk').filter(id=current_comment.post_id)[0]
        return f'/blog/{post.pk}/'


class DeleteAnothersCommentView(PermissionRequiredMixin, generic.DeleteView):
    permission_required = ('blog.deleteanotherscomment_Profile')
    permission_denied_message = "You haven't permission for this"
    model = Comment
    success_url = '/blog/'
    template_name = 'delete_comment_confirm.html'


class DetailAccountView(generic.DetailView):
    model = Profile
    context_object_name = 'profile_list'
    template_name = 'detail_account.html'


class EditAccountView(generic.UpdateView):
    form_class = AccountForm
    model = Profile
    template_name = 'edit_account.html'

    def get_success_url(self):
        pk = self.request.user.pk
        return f'/blog/user/{pk}'


class RegisterView(generic.View):

    def get(self, request, *args, **kwargs):
        form = ExtendedRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = ExtendedRegisterForm(request.POST, request.FILES)

        if form.is_valid():
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

            logger.info(f'new user was registered with name {name}, surname {surname} at {get_now()}')

            return redirect('/blog')

        form = ExtendedRegisterForm()
        return render(request, 'register.html', {'form': form})


class OurLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()
        logger.info(f'{user} was authenticated at {get_now()}')
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class OurLogoutView(LogoutView):
    template_name = 'logout.html'
