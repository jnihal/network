# Generated by Django 3.2 on 2021-05-21 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_follower'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='timestamp',
            field=models.DateField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]
