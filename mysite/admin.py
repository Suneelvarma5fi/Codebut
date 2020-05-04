
from django.contrib import admin

from polls.models import Questions
from blog.models import BlogPosts
class QuestionsAdmin(admin.ModelAdmin):
    fileds = ['pub_date','question_text']

admin.site.register(Questions,QuestionsAdmin)
admin.site.register(BlogPosts)