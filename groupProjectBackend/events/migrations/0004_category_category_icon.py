# Generated by Django 3.0.8 on 2020-10-25 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20201024_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_icon',
            field=models.URLField(default='https://via.placeholder.com/300.jpg', max_length=120),
        ),
    ]
