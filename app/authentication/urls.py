from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

router = routers.DefaultRouter()
# router.register(url, ViewSet, base_name='')


app_name = 'authentication'
urlpatterns = [
    path('signin/', views.obtain_auth_token),
    path('', include(router.urls)),
]
