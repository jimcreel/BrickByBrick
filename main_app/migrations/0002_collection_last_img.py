# Generated by Django 4.1.7 on 2023-04-06 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='last_img',
            field=models.CharField(default='https://i.imgur.com/2ZQ4U0i.png', max_length=250),
        ),
    ]
