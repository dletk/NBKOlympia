# Generated by Django 2.1.4 on 2019-01-08 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tangtoc', '0007_auto_20190108_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='value',
            field=models.IntegerField(blank=True, choices=[(10, 10), (20, 20), (30, 30)], null=True, verbose_name='Giá trị câu hỏi'),
        ),
    ]
