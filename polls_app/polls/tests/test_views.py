from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
import datetime

from polls.views import IndexView, DetailView, ResultsView
from polls.models import Question
from .utils import create_question


class QuestionIndexViewTests(TestCase):

    # TODO - exclude from publishing questions without choices 
    # TODO - Upon completion package the app: https://docs.djangoproject.com/en/3.2/intro/reusable-apps/

    def test_question_index_view_resolves_to_home_page_view(self):
        found = resolve('/polls/')
        self.assertEqual(found.func.view_class, IndexView) 

    def test_uses_home_template(self):
        response = self.client.get(reverse('polls:index'))
        self.assertTemplateUsed(response, 'polls/index.html')

    def test_question_index_view_returns_no_questions_message(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_question_index_view_returns_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_question_index_view_returns_no_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_question_index_view_returns_only_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
            )

    def test_question_index_view_returns_multiple_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)

        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):

    def test_detail_view_resolves_to_details_page_view(self):
        question = create_question()

        found = resolve('/polls/1/')
        self.assertEqual(found.func.view_class, DetailView) 

    def test_uses_detail_template(self):
        question = create_question()
        
        response = self.client.get(reverse('polls:detail', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'polls/detail.html')

    def test_detail_view_returns_no_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        # url = reverse('polls:detail', args=(future_question.id,))
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_detail_view_returns_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail',args=(past_question.id,))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)


class QuizResultslViewTests(TestCase):

    def test_results_view_resolves_to_home_page_view(self):
        question = create_question()
        found = resolve('/polls/1/results/')

        self.assertEqual(found.func.view_class, ResultsView) 

    def test_uses_results_template(self):
        question = create_question()
        
        response = self.client.get(reverse('polls:results', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'polls/results.html')

    def test_results_view_returns_no_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_results_view_returns_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:results',args=(past_question.id,))
        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)