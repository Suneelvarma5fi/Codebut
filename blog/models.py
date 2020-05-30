from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
# Create your models here.

class BlogPosts(models.Model):

    post_id = models.AutoField(primary_key=True)        #post_id works as primarykey
    post_title = models.CharField(max_length=150)     #post_title
    post_content = models.TextField() #content of the post
    pub_date = models.DateTimeField(default = timezone.now)  #published Date
    claps = models.IntegerField(default=0)     #claps for the post
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('blog-detail',kwargs={'pk':self.pk})


    def addclap(self):
        self.claps += 1
        return

    class Meta:
        verbose_name_plural = 'Blog Posts';