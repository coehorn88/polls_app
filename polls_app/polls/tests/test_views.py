from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
import datetime

from polls.views import IndexView, DetailView
from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

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


class DetailPageTest(TestCase):

    def test_root_view_resolves_to_home_page_view(self):
        question = Question.objects.create(
                question_text = "Test Question", 
                pub_date = timezone.now(),
            ).save()

        found = resolve('/polls/1/')
        self.assertEqual(found.func.view_class, DetailView) 

    def test_uses_detail_template(self):
        question = Question.objects.create(
                question_text = "Test Question", 
                pub_date = timezone.now(),
            ).save()
        
        response = self.client.get(reverse('polls:detail', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'polls/detail.html')
