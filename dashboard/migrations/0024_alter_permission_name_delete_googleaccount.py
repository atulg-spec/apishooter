# Generated by Django 4.2.7 on 2024-12-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_alter_permission_name_googleaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(choices=[('IMG_TO_PDF', 'Image to PDF'), ('HTML_TO_PDF', 'HTML to PDF'), ('HTML', 'HTML'), ('ONLY_IMG', 'Image as Content'), ('HTML_IMG', 'HTML to Image'), ('PDF', 'PDF'), ('HTML_TO_IMG_TO_PDF', 'HTML to Image to PDF'), ('HTML_TO_IMG', 'HTML to Image')], max_length=255),
        ),
        migrations.DeleteModel(
            name='GoogleAccount',
        ),
    ]