from django.utils import timezone
from rest_framework import viewsets, mixins, views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from app.surveys.models import Survey, Question
from app.surveys.serializers import SurveySerializer,\
     SurveyUpdateSerializer, QuestionListSerializer, \
     QuestionRetrieveCreateSerializer, QuestionUpdateSerializer, \
     SurveyDetailSerializer, UserResponseSetCreateSerializer
from app.utils.mixins import MultiSerializerViewSetMixin


class AdminSurveyViewSet(MultiSerializerViewSetMixin, 
                         mixins.ListModelMixin, 
                         mixins.CreateModelMixin, 
                         mixins.UpdateModelMixin, 
                         mixins.DestroyModelMixin, 
                         viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_action_classes = {
        'list': SurveySerializer,
        'create': SurveySerializer,
        'destroy': SurveySerializer,
        'update': SurveyUpdateSerializer,
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
    

class UserSurveyViewSet(MultiSerializerViewSetMixin,
                        viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_action_classes = {
        'list': SurveySerializer,
        'retrieve': SurveyDetailSerializer,
    }
    queryset = Survey.objects.all()

    def get_queryset(self):
        now = timezone.now()
        queryset = Survey.objects.filter(
            date_start__lte=now, date_end__gte=now
        )
        return queryset


class UserResponseSetAPIView(views.APIView):
    permission_classes = (AllowAny,)
    
    def get_serializer_context(self):
        return context

    def post(self, request, *args, **kwargs):
        serializer = UserResponseSetCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
