# Generated by Django 3.1.4 on 2021-04-20 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_contacts'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='Read',
            field=models.BooleanField(default=False),
        ),
    ]
