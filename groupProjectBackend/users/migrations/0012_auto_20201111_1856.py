# Generated by Django 3.0.8 on 2020-11-11 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20201107_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentorprofile',
            name='mentor_image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orgprofile',
            name='org_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]