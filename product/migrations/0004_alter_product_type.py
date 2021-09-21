# Generated by Django 3.2.7 on 2021-09-20 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_variation_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('V', 'Variable'), ('S', 'Simple')], default='V', max_length=1),
        ),
    ]
