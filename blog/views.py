from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from blog.forms import CommentForm, ExtendedRegisterForm, AccountForm, PostDocumentForm
from blog.models import Post, Comment, Profile, Category


class ListCategoryView(generic.ListView):

    def get(self, request, *args, **kwargs):
        category = kwargs['category']
        posts = Post.objects.filter(categories__name__contains=category).order_by('-created_on')
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
        queryset = queryset.order_by('-created_on')
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
        if form.cleaned_data['categories']:
            categories = Category.objects.create(name=form.cleaned_data['categories'])
            instance = Post.objects.get_or_create(title=kwargs['title'], body=kwargs['body'], profile=kwargs['profile'],
                                                  image=kwargs['image'])[0]
            instance.categories.set([categories])


class EditPostView(generic.UpdateView):
    form_class = PostDocumentForm
    model = Post
    template_name = 'edit_post.html'
    success_url = '/blog/'

    def form_valid(self, form):

        category_tokens = form.cleaned_data['categories'].split()
        edit_categories = set()

        for token in category_tokens:
            try:
                category = Category.objects.get(name=token)
            except Category.DoesNotExist:
                category = Category.objects.create(name=token)

            edit_categories.add(category)

        categories = []

        profile = self.request.user.profile
        title = form.cleaned_data.get('title')
        body = form.cleaned_data.get('body')
        image = form.cleaned_data.get('image')

        for category_to_add in edit_categories:
            categories.append(Category.objects.get_or_create(name=category_to_add.name)[0])

        Post.objects.filter(pk=self.object.pk).delete()

        instance = Post.objects.create(id=self.object.pk, title=title, body=body, profile=profile, image=image)
        instance.categories.set(categories)

        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        categories = ''
        object = self.get_object()

        post_categories = object.categories
        list_categories = self.add_category(post_categories)

        if list_categories:
            categories = ' '.join(list_categories)

        form_data = {
            'title': object.title,
            'body': object.body,
            'image': object.image,
            'categories': categories
        }
        form = PostDocumentForm(initial=form_data)

        return render(request, self.template_name, {'form': form})

    def add_category(self, post_categories):
        categories = []
        for category in post_categories.all():
            categories.append(Category.objects.filter(name=category.name)[0].name)
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
        form = CommentForm(request.POST)

        if form.is_valid():
            author = self.check_user_authenticated(request, form)

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

    def check_user_authenticated(self, request, form):
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
        post = Post.objects.filter(id=queryset.filter()[0].post_id)[0]
        return f'/blog/{post.pk}/'


class DeleteCommentView(generic.DeleteView):
    model = Comment
    template_name = 'delete_comment_confirm.html'

    def get_success_url(self):
        queryset = super().get_queryset()
        post = Post.objects.filter(id=queryset.filter()[0].post_id)[0]
        return f'/blog/{post.pk}/'


class DeleteAnothersCommentView(PermissionRequiredMixin, generic.DeleteView):
    permission_required = ('blog.deleteanotherscomment_Profile')
    permission_denied_message = "You haven't permission for this"
    model = Post
    success_url = '/blog/'
    template_name = 'delete_post_confirm.html'


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
            return redirect('/blog')
        else:
            form = ExtendedRegisterForm()
        return render(request, 'register.html', {'form': form})


class OurLoginView(LoginView):
    template_name = 'login.html'


class OurLogoutView(LogoutView):
    template_name = 'logout.html'
