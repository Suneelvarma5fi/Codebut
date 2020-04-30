from django.contrib import admin

from .models import Questions,Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text',]}),
        ('Date Information', {'fields': ['pub_date',]})
    ]
    inlines = [ChoiceInline]

admin.site.register(Questions,QuestionsAdmin)
admin.site.register(Choice)