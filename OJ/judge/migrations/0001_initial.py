# Generated by Django 4.0.5 on 2022-07-01 05:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Problem_id', models.PositiveBigIntegerField(default=0)),
                ('Title', models.CharField(max_length=50)),
                ('Description', models.TextField()),
                ('Input_Format', models.TextField()),
                ('Output_Format', models.TextField()),
                ('Constraint', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Input_File', models.FileField(upload_to='')),
                ('Output_file', models.FileField(upload_to='')),
                ('Problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judge.problem')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Submission_Time', models.DateTimeField(default=datetime.datetime.now)),
                ('Language', models.CharField(max_length=10)),
                ('Code', models.FileField(upload_to='')),
                ('Problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judge.problem')),
            ],
        ),
    ]
