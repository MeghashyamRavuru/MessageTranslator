# Generated by Django 5.1.7 on 2025-03-25 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0008_alter_customuser_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('te', 'Telugu'), ('hi', 'Hindi'), ('ta', 'Tamil'), ('kn', 'Kannada')], default='en', max_length=50),
        ),
    ]
