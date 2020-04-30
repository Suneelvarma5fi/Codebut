from django.shortcuts import render,get_object_or_404
from polls.models import Questions,Choice
from django.http import HttpResponse,HttpRequest,Http404,HttpResponseRedirect
from django.urls import reverse
#generic views
from django.views import generic
from django.utils import timezone

#returning the latest questions acc to publication date
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        '''return the most recent three questions'''
        return Questions.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Questions
    template_name = 'polls/details.html'

    def get_queryset(self):
        '''returns question objects which are on or before today'''
        return Questions.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Questions
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Questions.objects.filter(pub_date__lte=timezone.now())

def vote(request,id):
    question = get_object_or_404(Questions,pk=id)
    try:
        voted_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/details.html',{'questions':question,'error_message':"You didn't select any choice",})
    else:
        voted_choice.vote += 1
        voted_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
