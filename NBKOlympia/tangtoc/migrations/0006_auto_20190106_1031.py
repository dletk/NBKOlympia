# Generated by Django 2.1.4 on 2019-01-06 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tangtoc', '0005_auto_20181229_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='contestant',
            field=models.CharField(blank=True, choices=[('ts1', 'Thí sinh 1'), ('ts2', 'Thí sinh 2'), ('ts3', 'Thí sinh 3'), ('ts4', 'Thí sinh 4')], max_length=255),
        ),
        migrations.AlterField(
            model_name='answer',
            name='round',
            field=models.CharField(choices=[('tangtoc', 'Tăng tốc'), ('vcnv', 'VCNV'), ('khoidong', 'Khởi động'), ('vedich', 'Về đích'), ('', 'Empty')], max_length=255, verbose_name='Vòng thi'),
        ),
        migrations.AlterField(
            model_name='question',
            name='round',
            field=models.CharField(choices=[('tangtoc', 'Tăng tốc'), ('vcnv', 'VCNV'), ('khoidong', 'Khởi động'), ('vedich', 'Về đích')], max_length=255, verbose_name='Vòng thi'),
        ),
    ]
