from django.shortcuts import render

# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError
from .models import BlogPosts
from django.shortcuts import render
from django.db.models import Q

def homeview(request):

    sortby = request.POST.get('sortby', False)
    if sortby:
        sortby = '-'+sortby
        post_list = BlogPosts.objects.all().order_by(sortby)
    else:
        post_list = BlogPosts.objects.all().order_by('post_id')
    return render(request, 'blog/index.html', {'post_list': post_list,'error': False})


def detailedview(request, post_id):
    '''View after select the page'''

    post = BlogPosts.objects.get(post_id=post_id)
    title = post.post_title
    pub_date = post.pub_date
    claps = post.claps
    content = post.post_content

    frontend_reqs = {
        'post_id': post_id,
        'title': title,
        'pub_date': pub_date,
        'claps': claps,
        'content': content,
    }

    return render(request, 'blog/details.html', frontend_reqs)


def claps(request,post_id):

    post = BlogPosts.objects.get(pk=post_id)
    post_list = BlogPosts.objects.filter(~Q(post_id=post_id))
    post.claps += 1
    post.save()
    return render(request, 'blog/afterclap.html', {'post_list': post_list})
