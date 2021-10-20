from django.db import models
from django.conf import settings
from app.utils.mixins import CreatedUpdatedModelMixin


class Survey(CreatedUpdatedModelMixin):
    title = models.CharField(max_length=120)
    description = models.TextField()
    date_start = models.DateField(editable=False)
    date_end = models.DateField()

    def __str__(self) -> str:
        return self.title
    

class Question(CreatedUpdatedModelMixin):
    TEXT = 0
    SINGLE_CHOICE = 1
    MULTIPLE_CHOICE = 2
    TYPE_CHOICES = (
        (TEXT, 'Ответ текстотм'),
        (SINGLE_CHOICE, 'Ответ с выбором одного варианта'),
        (MULTIPLE_CHOICE, 'Ответ с выбором нескольких вариантов'),
    )
    survey = models.ForeignKey(
        Survey, related_name='questions', 
        on_delete=models.CASCADE
    )
    title = models.TextField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)

    def __str__(self) -> str:
        return self.title


class QuestionChoice(CreatedUpdatedModelMixin):
    question = models.ForeignKey(
        Question, related_name='choices', 
        on_delete=models.CASCADE
    )
    title = models.TextField()

    def __str__(self) -> str:
        return self.title


class UserResponseSet(CreatedUpdatedModelMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='response_sets', 
        on_delete=models.CASCADE
    )
    survey = models.ForeignKey(
        Survey, related_name='response_sets', 
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return '{} -> {}'.format(self.user, self.survey)


class UserResponse(CreatedUpdatedModelMixin):
    user_survey_response_set = models.ForeignKey(
        UserResponseSet, related_name='responses', 
        on_delete=models.CASCADE
    )
    # If Question.type is Multiple Choice or Signle Choice
    question_choice = models.ForeignKey(
        QuestionChoice, related_name='responses', 
        on_delete=models.SET_NULL, null=True
    )
    # If Question.type is Text
    question = models.ForeignKey(
        Question, related_name='responses', 
        on_delete=models.SET_NULL, null=True
    )
    text = models.TextField(null=True)

    def __str__(self) -> str:
        return self.user_survey_response_set
