from django.urls import include, path
from rest_framework import routers
from app.surveys.views import AdminSurveyViewSet


router = routers.DefaultRouter()
router.register(r'admin-surveys/', AdminSurveyViewSet)


app_name = 'surveys'
urlpatterns = [
    path('', include(router.urls)),
]
