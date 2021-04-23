# Generated by Django 3.1.4 on 2021-04-20 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_contacts_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='definition',
            name='Dictionary',
        ),
        migrations.CreateModel(
            name='group_new_word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Definition', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='index.definition')),
                ('Dictionary', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='index.dictionary')),
            ],
        ),
    ]