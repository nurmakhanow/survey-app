from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()


app_name = 'surveys'
urlpatterns = [
    path('', include(router.urls)),
]
