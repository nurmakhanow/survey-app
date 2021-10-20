from django.urls import include, path
from rest_framework import routers
from app.surveys.views import AdminSurveyViewSet, QuestionViewSet, UserSurveyViewSet


router = routers.DefaultRouter()
router.register(r'admin/surveys', AdminSurveyViewSet)
router.register(r'admin/questions', QuestionViewSet)
router.register(r'user/surveys', UserSurveyViewSet)


app_name = 'surveys'
urlpatterns = [
    path('', include(router.urls)),
]