from django.shortcuts import render, redirect

# Create your views here.
from .models import BlogPosts
from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user
from django.contrib.auth.models import User

class PostListView(LoginRequiredMixin,ListView):
    model = BlogPosts
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_ordering(self):
        if self.kwargs.get('sortby', False):
            ordering = '-'+self.kwargs['sortby']
        else:
            ordering = 'post_id'
        return ordering


class PostDetailView(DetailView):
    model = BlogPosts
    template_name = 'blog/details.html'



def claps(request, pk):
    post = get_object_or_404(BlogPosts,pk=pk)
    post_list = BlogPosts.objects.filter(author = post.author) #filter by author object
    post_list = post_list.filter(~Q(post_id=pk)).order_by('-claps') #filter by detail post and sort by popularity
    user = get_user(request)

    if user != post.author:
        post.addclap()
        post.save()

    frontend_reqs = {
        'object': post,
        'posts': post_list,
    }                           

    return render(request, 'blog/afterclap.html', frontend_reqs)

class UserPostView(PostListView):
    model = User
    template_name = 'blog/userpostsview.html'
    context_object_name = 'post_list'
    paginate_by = 3
    def get_queryset(self):
        user = get_object_or_404(self.model,username = self.kwargs['username'])
        return user.blogposts_set.all().order_by('-claps')


# CRUD SECTION ###################################################################

class PostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPosts
    fields = ['post_title', 'post_content']
    template_name = 'blog/createview.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPosts
    fields = ['post_title', 'post_content']
    template_name = 'blog/updateview.html'

    def post_id_original(self):
        return self.kwargs['pk']

    def form_valid(self, form):
        form.instance.post_id = self.post_id_original()
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