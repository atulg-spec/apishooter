# Generated by Django 4.2.7 on 2024-12-29 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0035_alter_messages_format_type_alter_permission_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='send_from',
            field=models.CharField(choices=[('API', 'API'), ('SMTP', 'SMTP'), ('RANDOM', 'RANDOM')], default='API', max_length=10),
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(choices=[('HTML_IMG_INLINE', 'HTML to Image Inline'), ('HTML_TO_PDF', 'HTML to PDF'), ('ONLY_IMG', 'Image as Content'), ('HTML_TO_IMG', 'HTML to Image'), ('IMG_TO_PDF', 'Image to PDF'), ('HTML_IMG', 'HTML with Image Attachment'), ('HTML', 'HTML'), ('PDF', 'PDF'), ('HTML_TO_IMG_TO_PDF', 'HTML to Image to PDF')], max_length=255),
        ),
    ]
