# Generated by Django 4.1.7 on 2023-04-04 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_remove_inventories_set_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory_set',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
