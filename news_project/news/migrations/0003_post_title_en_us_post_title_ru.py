# Generated by Django 5.0.6 on 2024-07-25 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_post_text_en_us_post_text_ru'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title_en_us',
            field=models.CharField(max_length=128, null=True, verbose_name='title post'),
        ),
        migrations.AddField(
            model_name='post',
            name='title_ru',
            field=models.CharField(max_length=128, null=True, verbose_name='title post'),
        ),
    ]
