# Generated by Django 3.1.7 on 2021-11-15 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glucose', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='glucoselevel',
            name='recording_type',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]