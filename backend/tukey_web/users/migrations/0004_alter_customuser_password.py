# Generated by Django 5.1.3 on 2024-11-29 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(default='', max_length=128),
        ),
    ]