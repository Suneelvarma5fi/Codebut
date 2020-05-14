from django.shortcuts import render

# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError
from .models import BlogPosts
from django.shortcuts import render
from django.db.models import Q

def homeview(request):

    def grouper(x):
        '''For the frontend grid comfortability'''

        y = [] #new list
        i = 0
        for j in range(3, len(x) + 1, 3):
            y.append(x[i:j])
            i = j
        if x[j:]: y.append(x[j:])
        return y   #return grouped list 3X3

    sortby = request.POST.get('sortby', False)
    if sortby:
        sortby = '-'+sortby
        post_list = BlogPosts.objects.all().order_by(sortby)
        post_list = grouper(post_list)
    else:
        post_list = BlogPosts.objects.all().order_by('post_id')
        post_list = grouper(post_list)
    return render(request, 'blog/index.html', {'post_list': post_list,'error': False})


def detailedview(request, post_id):
    '''View after select the page'''

    post = BlogPosts.objects.get(post_id=post_id)
    title = post.post_title
    pub_date = post.pub_date
    claps = post.claps
    content = post.post_content
    post_list = BlogPosts.objects.filter(~Q(post_id=post_id))

    frontend_reqs = {
        'post_id': post_id,
        'title': title,
        'pub_date': pub_date,
        'claps': claps,
        'content': content,
        'post_list':post_list,
    }

    return render(request, 'blog/details.html', frontend_reqs)


def claps(request,post_id):

    post = BlogPosts.objects.get(pk=post_id)
    title = post.post_title
    pub_date = post.pub_date
    content = post.post_content
    post_list = BlogPosts.objects.filter(~Q(post_id=post_id)).order_by('-claps')

    post.claps += 1
    post.save()

    frontend_reqs = {
        'post_id': post_id,
        'title': title,
        'pub_date': pub_date,
        'content': content,
        'post_list': post_list,
    }

    return render(request, 'blog/afterclap.html', frontend_reqs)