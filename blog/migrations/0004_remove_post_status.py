# Generated by Django 5.0.6 on 2024-06-01 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='status',
        ),
    ]
