# Generated by Django 3.1.7 on 2021-05-12 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_auto_20210512_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='facebook',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='github',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
