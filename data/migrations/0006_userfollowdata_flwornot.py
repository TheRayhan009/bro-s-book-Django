# Generated by Django 5.0.6 on 2024-10-17 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_userfollowdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfollowdata',
            name='flwOrNot',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
