from django.test import TestCase
from django.utils import timezone
import datetime

from polls.models import Question, Choice

class QuestionModelTest(TestCase):

    def create_question(self, question_text = "Test Question"):
        question = Question.objects.create(
            question_text = question_text, 
            pub_date = timezone.now(),
        )

        return question

    def test_can_save_quiz(self):
        ### Setup ###
        first_question = self.create_question()
        first_question.save()

        second_question = self.create_question()
        second_question.save()

        ### Assertion ###
        all_questions = Question.objects.all()
        self.assertEqual(all_questions.count(), 2)


    def test_string_representation(self):
        question = self.create_question()
        self.assertEqual(str(question), 'Test Question')

    def test_was_published_recently(self):
        question = self.create_question()
        self.assertEqual(question.was_published_recently(), True)

    def test_item_is_related_to_list(self):
        ### Setup ###
        question = self.create_question()
        choice = Choice.objects.create(question_id=1, choice_text='Choice1', votes=0)
        choice.question = question
        question.save()

        ### Assertion ###
        self.assertIn(choice, question.choice_set.all())        

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)