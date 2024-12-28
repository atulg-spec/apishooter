# Generated by Django 4.2.7 on 2024-12-25 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_messages_sender_name_messages_unsuscribe_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiencedata',
            name='tag',
            field=models.CharField(default='First Campaign', max_length=50),
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(choices=[('HTML_TO_IMG', 'HTML to Image'), ('PDF', 'PDF'), ('ONLY_IMG', 'Image as Content'), ('IMG_TO_PDF', 'Image to PDF'), ('HTML', 'HTML'), ('HTML_TO_IMG_TO_PDF', 'HTML to Image to PDF'), ('HTML_TO_PDF', 'HTML to PDF'), ('HTML_IMG', 'HTML to Image')], max_length=255),
        ),
    ]