# Generated by Django 3.1.7 on 2021-05-14 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0011_auto_20210514_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_pic',
            field=models.ImageField(default='', upload_to='authors/profile'),
        ),
    ]
