# Generated by Django 2.0 on 2020-10-30 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0005_datatracking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datatracking',
            name='blogtitle',
            field=models.CharField(max_length=200),
        ),
    ]