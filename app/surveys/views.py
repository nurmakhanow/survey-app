from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from app.surveys.models import Survey
from app.surveys.serializers import AdminSurveySerializer
from app.utils.mixins import MultiSerializerViewSetMixin


class AdminSurveyViewSet(mixins.ListModelMixin, 
                         mixins.CreateModelMixin, 
                         mixins.UpdateModelMixin, 
                         mixins.DestroyModelMixin, 
                         viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = AdminSurveySerializer
    queryset = Survey.objects.all().order_by('-date_start')
