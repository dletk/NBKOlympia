# Generated by Django 2.1.5 on 2019-01-22 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_myuser_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_thuky',
            field=models.BooleanField(default=False),
        ),
    ]
