# Generated by Django 2.1.2 on 2020-02-27 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearnerapp', '0004_auto_20200227_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='question',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='elearnerapp.Question'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='answer',
            field=models.CharField(default='E', max_length=5),
        ),
    ]
