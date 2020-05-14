from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('',views.homeview,name='homeview'),
    path('<int:post_id>/',views.detailedview,name = 'detailedview'),
    path('<int:post_id>/clap/',views.claps,name = 'claps'),
]