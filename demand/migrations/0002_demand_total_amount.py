# Generated by Django 3.2.7 on 2021-10-27 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='total_amount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
