# Generated by Django 4.2.7 on 2024-11-17 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_messages_attachment_content'),
    ]

    operations = [
        migrations.DeleteModel(
            name='tags_data',
        ),
    ]
