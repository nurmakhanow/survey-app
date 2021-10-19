from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from app.authentication.forms import UserChangeForm, UserCreationForm
from app.surveys.models import Survey


User = get_user_model()


@admin.register(Survey)
class SurveyAdmin(auth_admin.UserAdmin):
    list_display = ('id', 'title', 'date_start', 'date_end',)

