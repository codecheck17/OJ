# Generated by Django 4.0.5 on 2022-07-02 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0003_alter_testcase_input_file_alter_testcase_output_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='Input_File',
            field=models.FileField(upload_to='testfiles/input/'),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='Output_file',
            field=models.FileField(upload_to='testfiles/output/'),
        ),
    ]
