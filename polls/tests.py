
import datetime
from django.test import TestCase
from django.utils import timezone
from django.test import Client
from .models import Questions
from django.urls import reverse

class QuestionsModelTest(TestCase):

    def test_how_recent_with_future_question(self):

        '''testing whether future questions considered as recent'''

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Questions(pub_date=time)
        self.assertIs(future_question.how_recent(),False)

    '''testing the boundary values of the publication date'''

    def test_how_recent_an_old_question(self):

        time = timezone.now()-datetime.timedelta(days=1,seconds=1)
        old_question = Questions(pub_date=time)
        self.assertIs(old_question.how_recent(),False)

    def test_how_recent_a_recent_question(self):

        time = timezone.now()-datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_question = Questions(pub_date=time)
        self.assertIs(recent_question.how_recent(),True)

def create_question(question_text,days):
    '''creating a question, based on the kind of test we're making'''
    time = timezone.now()+datetime.timedelta(days=days)
    return Questions.objects.create(question_text=question_text,pub_date=time)

class QuestionsIndexViewTest(TestCase):
    '''indexview testing class'''

    def test_no_questions(self):
        '''testing the view when there're no questions'''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'There are no polls right now')
        self.assertQuerysetEqual(response.context['question_list'],[])

    def test_past_questions(self):
        '''testing the view for past questions'''
        create_question(question_text = 'Past Question',days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'],['<Questions: Past Question>'])

    def test_future_questions(self):
        '''testing view for future Questions'''
        create_question(question_text = 'Future Question',days = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,'There are no polls right now')
        self.assertQuerysetEqual(response.context['question_list'],[])

    def test_past_future_questions(self):
        '''testing view for both future and past Questions'''

        create_question(question_text = 'Past Question',days = -39)
        create_question(question_text = 'Future Question',days = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'],['<Questions: Past Question>'])

    def test_two_past_questions(self):
        '''testing fot two past questions'''
        create_question(question_text = 'Past Question 1',days = -30)
        create_question(question_text = 'Past Question 2',days = -50)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['question_list'],['<Questions: Past Question 1>','<Questions: Past Question 2>'])

class QuestionsDetailViewTest(TestCase):
    '''testing the detailed view'''

    def test_past_questions(self):
        '''test for past question'''

        past_question = create_question(question_text='Past Question',days = -30)
        url = reverse('polls:details', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_future_questions(self):
        '''test for future question'''

        future_question = create_question(question_text = 'Future Question',days = 30)
        url = reverse('polls:details',args = (future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

class QuestionsResultsView(TestCase):
    '''testing the results view'''

    def test_past_questions(self):
        past_question = create_question(question_text='Past Question',days = -32)
        url = reverse('polls:results',args = (past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,past_question.question_text)

    def test_future_questions(self):
        future_question = create_question(question_text='Future Question',days = 30)
        url = reverse('polls:results',args = (future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
