from rest_framework import serializers
from app.surveys.models import Question, QuestionChoice, Survey, UserResponse, UserResponseSet
from rest_framework.exceptions import ValidationError


class SurveySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    date_start = serializers.DateField(required=True)
    date_end = serializers.DateField(required=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'date_start', 'date_end',)


class SurveyUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    date_end = serializers.DateField(required=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'date_start', 'date_end',)


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ('id', 'title',)


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'type', 'choices',)


class SurveyDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'date_start', 'date_end', 'questions',)


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
    choices = QuestionChoiceRetrieveCreateSerializer(many=True, allow_null=True)

    class Meta:
        model = Question
        fields = ('id', 'survey_id', 'title', 'type', 'choices',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['survey'] = validated_data.pop('survey_id')
        choices = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        for c in choices:
            QuestionChoice.objects.create(question=question, **c)
        return question


class QuestionChoiceUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)

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
        instance.save()
        choices = validated_data.pop('choices')
        # Create QuestionChoice if there is no ID in db
        to_create = list()
        # Delete if QuestionChoice.ID in db but not present in data
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


class UserResponseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ('id', 'question_choices', 'question_id', 'text',)


class UserResponseCreateSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)
    choices = serializers.ListField(child=serializers.IntegerField(), required=True)

    class Meta:
        model = UserResponse
        fields = ('id', 'choices', 'question_id', 'text',)

    def validate(self, attrs):
        # Remove duplicated ids & check if QuestionChoice with such ids exist
        choices = set(attrs['choices'])
        if not QuestionChoice.objects.filter(id__in=attrs['choices']).count() == len(attrs['choices']):
            raise ValidationError({'choices': 'at least one object not found or same, check for duplicates'})
        return attrs

    def to_representation(self, instance):
        return UserResponseReadSerializer(instance).data



class UserResponseSetCreateSerializer(serializers.Serializer):
    survey_id = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all(), required=True)
    anonymous_user_id = serializers.IntegerField(required=False)
    responses = UserResponseCreateSerializer(many=True, required=True)

    def validate(self, attrs):
        survey = attrs['survey_id']
        # Text, single choice & multiple choice 
        text_type_qs_ids = survey.questions.filter(type=Question.TEXT).values_list('id', flat=True) 
        sc_type_qs_ids = survey.questions.filter(type=Question.SINGLE_CHOICE).values_list('id', flat=True)
        mc_type_qs_ids = survey.questions.filter(type=Question.MULTIPLE_CHOICE).values_list('id', flat=True)
        errors = dict()
        for resp in attrs['responses']:
            question_id = resp['question_id'].id
            if question_id in text_type_qs_ids and len(resp['choices']) > 0:
                errors['choices'] = ['must be empty due to Question.type (Text)']
            if question_id in sc_type_qs_ids and len(resp['choices']) > 1:
                err = 'must not contain more than 1 value due to Question.type (Single Choice)'
                errors['choices'] = [err]
            if question_id in mc_type_qs_ids and resp.get('text'):
                err = 'must be None due to Question.type (Multiple Choice)'
                errors['text'] = [err]
            if question_id in sc_type_qs_ids and resp.get('text'):
                err = 'must be None due to Question.type (Single Choice)'
                errors['text'] = [err]
        if errors:
            raise ValidationError(errors)
        return attrs

    def create(self, validated_data):
        responses = validated_data.pop('responses')
        user = None
        request = self.context["request"]
        if not validated_data.get('anonymous_user_id') and request.user.is_authenticated:
            validated_data['user'] = request.user
        validated_data['survey'] = validated_data.pop('survey_id')
        instance = UserResponseSet.objects.create(**validated_data)
        # Create UserResponses
        to_create = list()
        for resp in responses:
            question = resp.get('question_id')
            text = resp.get('text')
            selected_choices = resp.get('choices')
            if selected_choices:
                r = UserResponse.objects.create(
                    user_response_set=instance, 
                )
                r.question_choices.add(*selected_choices)
            else:
                to_create.append(
                    UserResponse(
                        user_response_set=instance, 
                        question=question, text=text, 
                    )
                )
        UserResponse.objects.bulk_create(to_create)
        return instance



class UserQuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'type', 'choices',)


class UserResponseSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    def get_question(self, instance):
        question = None
        if instance.question:
            question = instance.question
        elif instance.question_choices.first():
            question = instance.question_choices.first().question
        return UserQuestionSerializer(question).data

    class Meta:
        model = UserResponse
        fields = ('id', 'question', 'text', 'question_choices',)


class UserResponseSetSerializer(serializers.ModelSerializer):
    survey_title = serializers.CharField(source='survey.title')
    responses = UserResponseSerializer(many=True)

    class Meta:
        model = UserResponseSet
        fields = ('id', 'user', 'anonymous_user_id', 'survey', 'survey_title', 'responses',)


class AnonymousUserIdQueryParamSerializer(serializers.Serializer):
    anonymous_user_id = serializers.IntegerField(required=False)
