# Generated by Django 4.2.7 on 2024-10-14 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_delete_messages_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='frequency',
            field=models.PositiveIntegerField(default=10),
        ),
    ]
