# Generated by Django 2.1.1 on 2018-11-14 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
