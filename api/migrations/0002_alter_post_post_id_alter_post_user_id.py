# Generated by Django 4.0.5 on 2022-06-12 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='user_id',
            field=models.CharField(max_length=255),
        ),
    ]
