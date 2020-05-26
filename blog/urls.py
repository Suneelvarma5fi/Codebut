from django.urls import path
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostView
from . import views
#app_name = 'blog'
urlpatterns = [
	path('',PostListView.as_view(),name='blog-home'),
    path('<str:sortby>/',PostListView.as_view(),name='blog-home'),
    path('post/<int:pk>/',PostDetailView.as_view(),name = 'blog-detail'),
    path('<int:pk>/clap',views.claps,name = 'blog-claps'),
    path('create/new/',PostCreateView.as_view(),name = 'post-create'),
    path('update/<int:pk>/',PostUpdateView.as_view(),name = 'post-update'),
    path('delete/<int:pk>/',PostDeleteView.as_view(),name = 'post-delete'),
    path('user/<int:userid>/',UserPostView.as_view(),name = 'user-posts')
]