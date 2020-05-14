from rest_framework import serializers
from api_v1 import models

class QuestionOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionOptions
        fields = ('id', 'text', 'question')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'options', 'user', 'question', 'text')

class QuestionSerializer(serializers.ModelSerializer):
    questionoptions_set = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = models.Question
        fields = ('id', 'question', 'survey', 'questionoptions_set', 'type')

class SurveySerializer(serializers.ModelSerializer):
    question_set = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.Survey
        fields = ('id', 'title', 'description', 'question_set', 'start_date', 'end_date')