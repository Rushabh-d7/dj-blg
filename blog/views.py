from django.shortcuts import render, redirect,get_object_or_404
from django.views import generic
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Comment
from .forms import BlogForm, CommentForm

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
        context['comments'] = self.object.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=self.object.slug)
        return self.get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CreatePost(generic.View):
    form_class = BlogForm
    template_name = 'blog/create_blog.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(f"{request.user.username}_{post.title}")
            post.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})
