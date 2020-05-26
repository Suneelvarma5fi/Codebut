from django.shortcuts import render, redirect

# Create your views here.
from .models import BlogPosts
from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user


class PostListView(ListView,LoginRequiredMixin):
    model = BlogPosts
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_ordering(self):
        if self.kwargs.get('sortby', False):
            ordering = self.kwargs['sortby']
        else:
            ordering = 'post_id'
        return ordering


class PostDetailView(DetailView):
    model = BlogPosts
    template_name = 'blog/details.html'



def claps(request, pk):
    post = get_object_or_404(BlogPosts,pk=pk)
    post_list = BlogPosts.objects.filter(~Q(post_id=pk)).order_by('-claps')
    user = get_user(request)

    if user != post.author:
        post.claps += 1
        post.save()

    frontend_reqs = {
        'object': post,
        'posts': post_list,
    }                           

    return render(request, 'blog/afterclap.html', frontend_reqs)

class UserPostView(PostListView):
    model = BlogPosts
    template_name = 'blog/userpostsview.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return self.model.objects.filter(author = self.kwargs['userid'])

# CRUD SECTION ###################################################################

class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPosts
    fields = ['post_title', 'post_content']
    template_name = 'blog/createview.html'

    def form_valid(self, form):
        form.instance.post_id = self.request.user.pk
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPosts
    fields = ['post_title', 'post_content']
    template_name = 'blog/updateview.html'

    def form_valid(self, form):
        form.instance.post_id = self.request.user.pk
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPosts
    template_name = 'blog/deleteview.html'
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
