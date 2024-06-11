from django.shortcuts import render, redirect,get_object_or_404
from django.views import generic, View
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Comment, Like
from .forms import BlogForm, CommentForm
from django.contrib.auth.models import User

class PostList(generic.ListView):
    queryset = Post.objects.order_by('-created_on')
    template_name = 'blog/blogs_index.html'
    context_object_name = 'posts'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.filter(parent__isnull=True)
        context['liked'] = self.object.likes.filter(user=self.request.user).exists()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        self.object = self.get_object()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=self.object.slug)
        return self.get(request, *args, **kwargs)


class UserList(generic.ListView):
    model = User
    template_name = 'blog/user_list.html'
    context_object_name = 'users'

class UserPosts(generic.ListView):
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=self.user).order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        return context


@method_decorator(login_required, name='dispatch')
class CreatePost(generic.View):
    form_class = BlogForm
    template_name = 'blog/create_blog.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(f"{request.user.username}_{post.title}")
            post.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class DeletePost(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.author == request.user:
            post.delete()
        return redirect('home')

@method_decorator(login_required, name='dispatch')
class DeleteComment(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author == request.user:
            comment.delete()
        return redirect('post_detail', slug=comment.post.slug)


@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('post_detail', slug=slug)