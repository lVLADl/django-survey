from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True, default=datetime.today().strftime('%Y-%m-%d'))
    end_date = models.DateField(blank=True, null=True, default="{}-{}-{}".format(datetime.today().year, str(int(datetime.today().month)+1), datetime.today().day))

    is_started = models.BooleanField(blank=True, null=True, default=False)
    is_finished = models.BooleanField(blank=True, null=True, default=False)

    @staticmethod
    def get_active_surveys():
        from datetime import datetime
        current_date = datetime.today().strftime('%Y-%m-%d')
        return Survey.objects.all().filter(start_date__lte=current_date).filter(end_date__gte=current_date)
    def __str__(self):
        return "{}".format(self.question_set.all())

class Question(models.Model):
    TEXT_ANSWER = 'TA'
    CHOICE_ANSWER = 'CA'
    CHOICES_ANSWER = 'CSA'

    TYPE = (
        (TEXT_ANSWER, 'Answer with text'),
        (CHOICE_ANSWER, 'Answer with choice'),
        (CHOICES_ANSWER, 'Answer with multiple choices')
    )

    # Fields
    type = models.CharField(max_length=55, choices=TYPE, default=CHOICE_ANSWER)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=155)
    id = models.AutoField(primary_key=True)
    def __str__(self):
        options = ''
        for o in self.questionoptions_set.all():
            options += "[{}]-{}; ".format(o.id, o.text)
        return "id={},{}: |{}".format(self.id, self.question, options)

class QuestionOptions(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=250)

    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return '{'+ str(self.id) +'}' + " {}".format(self.text)


class Answer(models.Model):
    user = models.ForeignKey('AnonymousUser', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    options = models.ManyToManyField(QuestionOptions, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'question']),
        ]
    def __str__(self):
        return "[{}] {}...: {}".format(self.user, str(self.question)[0:40], self.options if self.options else self.text)


class AnonymousUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    def __str__(self):
        return str(self.id)