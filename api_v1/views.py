from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from setuptools.command.alias import alias

from . import models, serializers

from rest_framework import generics, response, views, status, permissions, decorators
# Create your views here

def newClient(request):
    anonymous_user = models.AnonymousUser.objects.create()
    return JsonResponse(data={'id': anonymous_user.id})

class SurveyView(views.APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    def get(self, request):
        survey = models.Survey.get_active_surveys()
        serializer = serializers.SurveySerializer(survey, many=True)
        return response.Response(serializer.data)
    def post(self, request):
        serializer = serializers.SurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SurveyDetailView(views.APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, survey_id):
        survey = models.Survey.objects.get(pk=survey_id)
        serializer = serializers.SurveySerializer(survey)
        return response.Response(serializer.data)
    def post(self, request, survey_id):
            data_extended = {
                'survey': survey_id
            }
            for k,v in request.data.items():
                data_extended[k]=v

            serializer = serializers.QuestionSerializer(data=data_extended)

            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, survey_id):
            from datetime import datetime
            survey = models.Survey.objects.get(pk=survey_id)
            serializer = serializers.SurveySerializer(survey, data=request.data)
            if serializer.is_valid():
                today = datetime.today()#.strftime('%Y-%m-%d')
                if 'start_date' in request.data:
                    if survey.is_started or survey.is_finished or datetime.strptime("{}-{}-{}".format(survey.start_date.year, survey.start_date.month, survey.start_date.day), '%Y-%m-%d') < datetime.strptime("{}-{}-{}".format(today.year, today.month, today.day), '%Y-%m-%d'):
                        return response.Response({'error': 'already started/finished'}, status.HTTP_400_BAD_REQUEST)
                    start_date = datetime.strptime(request.data['start_date'], '%Y-%m-%d')
                if 'end_date' in request.data:
                    if survey.is_started or survey.is_finished or datetime.strptime("{}-{}-{}".format(survey.end_date.year, survey.end_date.month, survey.end_date.day), '%Y-%m-%d') < datetime.strptime("{}-{}-{}".format(today.year, today.month, today.day), '%Y-%m-%d'):
                        return response.Response({'error': 'already started/finished'}, status.HTTP_400_BAD_REQUEST)
                    end_date = datetime.strptime(request.data['end_date'], '%Y-%m-%d')

                serializer.save()
                return response.Response(serializer.data)
            else:
                return response.Response(serializer.errors, status=400)
    def delete(self, request, survey_id):
        survey = models.Survey.objects.get(pk=survey_id)
        survey.delete()
        return response.Response(status=204)


class QuestionView(views.APIView):
    def get(self, request, **kwargs):
        question = models.Question.objects.get(pk=kwargs['question_id'])
        serializer = serializers.QuestionSerializer(question)

        return response.Response(serializer.data)
    def post(self, request, **kwargs):
        # Answer the question
        question = models.Question.objects.get(pk=kwargs['question_id'])
        data_extended = {
            'question': question.id,
        }
        for k, v in request.data.items():
            if k != 'options':
                data_extended[k] = v

        serializer = serializers.AnswerSerializer(data=data_extended)
        already_answered = models.Answer.objects.filter(question__id=data_extended['question']).filter(user__id=data_extended['user']).count()>0
        if serializer.is_valid() and not already_answered:
            an = serializer.save()
            options = []
            answer = models.Answer.objects.get(pk=an.id)
            if question.type == question.TEXT_ANSWER:
                answer.text = request.POST['text']
            if question.type == question.CHOICES_ANSWER:
                options = str(request.POST['options']).split(',')
                for option in options:
                    qo = models.QuestionOptions.objects.get(pk=option)
                    answer.options.add(qo)

            if question.type == question.CHOICE_ANSWER:
                qo = models.QuestionOptions.objects.get(pk=str(request.POST['options']))
                answer.options.add(qo)

            answer.save()

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if already_answered:
                return response.Response({'error': 'already answered'},
                                         status=status.HTTP_400_BAD_REQUEST)
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.permission_classes(permissions.IsAuthenticatedOrReadOnly)
    def delete(self, request, **kwargs):

        survey = models.Survey.objects.get(pk=kwargs['survey_id'])
        survey.delete()
        return response.Response(status=204)
    @decorators.permission_classes(permissions.IsAuthenticatedOrReadOnly)
    def put(self, request, **kwargs):
        question = models.Question.objects.get(pk=kwargs['question_id'])
        serializer = serializers.QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors, status=400)

class OptionView(views.APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, **kwargs):
        qo = models.QuestionOptions.objects.get(pk=kwargs['option_id'])
        serializer = serializers.QuestionOptionsSerializer(qo)
        return response.Response(serializer.data)

    def post(self, request, **kwargs):
        question = models.Question.objects.get(pk=kwargs['question_id'])
        data_extended = {
            'question': str(question.id)
        }
        for k, v in request.data.items():
            data_extended[k] = v
        serializer = serializers.QuestionOptionsSerializer(data=data_extended)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        option = models.QuestionOptions.objects.get(pk=kwargs['option_id'])
        serializer = serializers.QuestionOptionsSerializer(option, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors, status=400)

    def delete(self, request, **kwargs):
        option = models.QuestionOptions.objects.get(pk=kwargs['option_id'])
        option.delete()
        return response.Response(status=204)
def user_surveys(request, user_id):
    # return models.Survey.objects.all()
    surveys = models.Survey.objects.filter(question__answer__user=user_id).distinct()
    out = []
    for survey in surveys:
        questions = survey.question_set.all()
        question_view = []

        for q in questions:
            answer_instance = models.Answer.objects.filter(user_id=user_id).filter(question__id=q.id).first()
            answer = ''
            if answer_instance:
                if q.type == q.TEXT_ANSWER:
                    answer = answer_instance.text
                elif q.type == q.CHOICE_ANSWER:
                    answer = str(answer_instance.options.all().first())
                elif q.type == q.CHOICES_ANSWER:
                    for option in answer_instance.options.all():
                        answer += "{}|".format(option.text)

            question_view.append({q.question: answer})
        out.append({
            survey.id: question_view
        })
    return HttpResponse(out)