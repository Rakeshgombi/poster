# Generated by Django 3.1.7 on 2021-05-14 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0010_auto_20210514_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_pic',
            field=models.ImageField(default='', upload_to='authors/<bound method ForeignKey.get_attname of <django.db.models.fields.related.OneToOneField>>'),
        ),
    ]
