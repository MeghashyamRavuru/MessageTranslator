# Generated by Django 5.1.7 on 2025-04-04 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0009_alter_customuser_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='deleted_by',
            field=models.JSONField(default=list),
        ),
    ]
