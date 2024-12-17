# Generated by Django 4.2.7 on 2024-12-01 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_sitesettings_login_image_alter_permission_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='file_name',
            field=models.CharField(default='file', max_length=150),
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(choices=[('IMG_TO_PDF', 'Image to PDF'), ('PDF', 'PDF'), ('ONLY_IMG', 'Image as Content'), ('HTML_IMG', 'HTML to Image'), ('HTML_TO_PDF', 'HTML to PDF'), ('HTML', 'HTML'), ('HTML_TO_IMG', 'HTML to Image'), ('HTML_TO_IMG_TO_PDF', 'HTML to Image to PDF')], max_length=255),
        ),
    ]