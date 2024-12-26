# Generated by Django 4.2.7 on 2024-12-25 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_campaign_audience_data_campaign_send_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.CharField(choices=[('success', 'success'), ('processing', 'processing'), ('created', 'created')], default='created', max_length=12),
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(choices=[('PDF', 'PDF'), ('HTML', 'HTML'), ('HTML_TO_PDF', 'HTML to PDF'), ('IMG_TO_PDF', 'Image to PDF'), ('HTML_TO_IMG', 'HTML to Image'), ('HTML_IMG', 'HTML to Image'), ('ONLY_IMG', 'Image as Content'), ('HTML_TO_IMG_TO_PDF', 'HTML to Image to PDF')], max_length=255),
        ),
    ]
