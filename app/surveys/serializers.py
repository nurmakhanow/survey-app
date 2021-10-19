from rest_framework import serializers
from app.surveys.models import Survey


class AdminSurveySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    date_start = serializers.DateField(required=True)
    date_end = serializers.DateField(required=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'date_start', 'date_end',)


class AdminSurveyUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    date_end = serializers.DateField(required=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'date_start', 'date_end',)
