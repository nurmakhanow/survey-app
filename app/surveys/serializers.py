from rest_framework import serializers
from app.surveys.models import Question, QuestionChoice, Survey


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


class QuestionListSerializer(serializers.ModelSerializer):
    survey_id = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all(), required=True)

    class Meta:
        model = Question
        fields = ('id', 'survey_id', 'title', 'type',)
        read_only_fields = ('id',)


class QuestionChoiceRetrieveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ('id', 'title',)


class QuestionRetrieveCreateSerializer(serializers.ModelSerializer):
    survey_id = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all(), required=True)
    choices = QuestionChoiceRetrieveCreateSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'survey_id', 'title', 'type', 'choices',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['survey'] = validated_data.pop('survey_id')
        choices = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        for c in choices:
            # c_id = c.pop('id')
            QuestionChoice.objects.create(question=question, **c)
        return question


class QuestionChoiceUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True, allow_null=True)

    class Meta:
        model = QuestionChoice
        fields = ('id', 'title',)


class QuestionUpdateSerializer(serializers.ModelSerializer):
    survey_id = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all(), required=True)
    choices = QuestionChoiceUpdateSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'survey_id', 'title', 'type', 'choices',)
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        instance.survey = validated_data.get('survey_id', instance.survey)
        instance.title = validated_data.get('title', instance.title)
        instance.type = validated_data.get('type', instance.type)
        choices = validated_data.pop('choices')
        to_create = list()
        to_delete_ids = list(instance.choices.values_list('id', flat=True))
        for c in choices:
            c_id = c.get('id')
            if c_id:
                to_delete_ids.remove(c_id)
                QuestionChoice.objects.filter(id=c_id).update(title=c.get('title'))
            else:
                to_create.append(QuestionChoice(title=c.get('title'), question=instance))
        QuestionChoice.objects.bulk_create(to_create)
        choice_ids = instance.choices.values_list('id', flat=True)
        instance.choices.filter(id__in=to_delete_ids).delete()        
        return instance
