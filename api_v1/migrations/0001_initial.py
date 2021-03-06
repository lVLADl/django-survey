# Generated by Django 3.0.3 on 2020-05-14 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousUser',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('type', models.CharField(choices=[('TA', 'Answer with text'), ('CA', 'Answer with choice'), ('CSA', 'Answer with multiple choices')], default='CA', max_length=55)),
                ('question', models.CharField(max_length=155)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(blank=True, default='2020-05-14', null=True)),
                ('end_date', models.DateField(blank=True, default='2020-6-14', null=True)),
                ('is_started', models.BooleanField(blank=True, default=False, null=True)),
                ('is_finished', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOptions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=250)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v1.Question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api_v1.Survey'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('options', models.ManyToManyField(blank=True, null=True, to='api_v1.QuestionOptions')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v1.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v1.AnonymousUser')),
            ],
        ),
        migrations.AddIndex(
            model_name='answer',
            index=models.Index(fields=['user', 'question'], name='api_v1_answ_user_id_7cc903_idx'),
        ),
    ]
