# Generated by Django 3.2.3 on 2021-05-17 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0020_alter_profile_display_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_pic',
            field=models.FileField(upload_to=''),
        ),
    ]