from django.db import models

# Create your models here.

class BlogPosts(models.Model):

    post_id = models.IntegerField(primary_key=True)        #post_id works as primarykey
    post_title = models.CharField(max_length=150)     #post_title
    post_content = models.CharField(max_length=1500) #content of the post
    pub_date = models.DateTimeField(auto_now = True)  #published Date
    claps = models.IntegerField(default=0)            #claps for the post

    def __str__(self):
        return self.post_title

    class Meta:
        verbose_name_plural = 'Blog Posts'