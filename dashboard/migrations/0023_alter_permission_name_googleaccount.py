# Generated by Django 4.2.7 on 2024-12-13 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0022_messages_file_name_alter_permission_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(choices=[('PDF', 'PDF'), ('HTML', 'HTML'), ('HTML_TO_PDF', 'HTML to PDF'), ('IMG_TO_PDF', 'Image to PDF'), ('HTML_TO_IMG_TO_PDF', 'HTML to Image to PDF'), ('ONLY_IMG', 'Image as Content'), ('HTML_TO_IMG', 'HTML to Image'), ('HTML_IMG', 'HTML to Image')], max_length=255),
        ),
        migrations.CreateModel(
            name='GoogleAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField()),
                ('refresh_token', models.TextField()),
                ('token_expiry', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]