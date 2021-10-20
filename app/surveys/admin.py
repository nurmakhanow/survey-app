from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from app.authentication.forms import UserChangeForm, UserCreationForm
from app.surveys.models import Survey, Question, QuestionChoice, UserResponseSet, UserResponse


User = get_user_model()


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_start', 'date_end',)
    readonly_fields = ('id', 'date_start',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'survey',)
    readonly_fields = ('id',)


@admin.register(QuestionChoice)
class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'title',)
    readonly_fields = ('id',)


@admin.register(UserResponseSet)
class UserResponseSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'anonymous_user_id', 'survey',)
    readonly_fields = ('id',)


@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_response_set', 'question', 'text',)
    readonly_fields = ('id',)
