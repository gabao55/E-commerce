# Generated by Django 3.2.7 on 2021-09-16 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_variation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variation',
            options={'verbose_name': 'Variation', 'verbose_name_plural': 'Variations'},
        ),
    ]
