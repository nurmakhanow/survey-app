from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from app.surveys.models import Survey
from app.surveys.serializers import AdminSurveySerializer, AdminSurveyUpdateSerializer
from app.utils.mixins import MultiSerializerViewSetMixin


class AdminSurveyViewSet(MultiSerializerViewSetMixin, 
                         mixins.ListModelMixin, 
                         mixins.CreateModelMixin, 
                         mixins.UpdateModelMixin, 
                         mixins.DestroyModelMixin, 
                         viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_action_classes = {
        'list': AdminSurveySerializer,
        'create': AdminSurveySerializer,
        'destroy': AdminSurveySerializer,
        'update': AdminSurveyUpdateSerializer,
    }
    queryset = Survey.objects.all().order_by('-date_start')
