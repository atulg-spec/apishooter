# Generated by Django 4.2.7 on 2024-11-16 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_messages_attachment_messages_format_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='attachment_content',
            field=models.TextField(default=''),
        ),
    ]