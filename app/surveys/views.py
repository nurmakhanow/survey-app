from django.utils import timezone
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny
from app.surveys.models import Survey, Question
from app.surveys.serializers import AdminSurveySerializer,\
     AdminSurveyUpdateSerializer, QuestionListSerializer, \
     QuestionRetrieveCreateSerializer, QuestionUpdateSerializer
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


class QuestionViewSet(MultiSerializerViewSetMixin, 
                      viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_action_classes = {
        'list': QuestionListSerializer,
        'retrieve': QuestionRetrieveCreateSerializer,
        'create': QuestionRetrieveCreateSerializer,
        'update': QuestionUpdateSerializer,
    }
    queryset = Question.objects.prefetch_related('choices')

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            survey_id = self.request.query_params.get('survey_id')
            if survey_id:
                queryset = queryset.filter(survey_id=survey_id)
        return queryset
    