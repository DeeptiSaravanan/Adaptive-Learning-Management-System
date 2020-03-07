# Generated by Django 2.1.2 on 2020-03-02 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearnerapp', '0014_auto_20200302_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='elearnerapp.Questionnaire'),
        ),
        migrations.AddField(
            model_name='useranswer',
            name='ques',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='elearnerapp.Question'),
        ),
    ]
