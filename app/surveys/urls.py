from django.urls import include, path
from rest_framework import routers
from app.surveys.views import AdminSurveyViewSet, QuestionViewSet, \
    UserSurveyViewSet, UserResponseSetAPIView, UserResponseSetSurveyViewSet


router = routers.DefaultRouter()
router.register(r'admin/surveys', AdminSurveyViewSet)
router.register(r'admin/questions', QuestionViewSet)
router.register(r'user/surveys', UserSurveyViewSet)
router.register(r'surveys/res', UserResponseSetSurveyViewSet)


app_name = 'surveys'
urlpatterns = [
    path('user/responses/', UserResponseSetAPIView.as_view()),
    path('', include(router.urls)),
]
