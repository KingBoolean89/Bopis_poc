# Generated by Django 3.1.7 on 2021-04-30 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20210428_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pushToken',
            field=models.CharField(default='Expo12345', max_length=50),
        ),
    ]
