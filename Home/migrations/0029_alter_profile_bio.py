# Generated by Django 3.2.3 on 2021-06-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0028_alter_profile_display_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(default='', max_length=300),
        ),
    ]