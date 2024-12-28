from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

status_choices = [
        ('success', 'success'),
        ('processing', 'processing'),
        ('created', 'created'),
    ]

# Define the permission map as a constant
PERMISSION_MAP = {
    ('HTML', 'HTML'),
    ('HTML_IMG', 'HTML with Image Attachment'),
    ('HTML_TO_IMG', 'HTML to Image'),
    ('HTML_IMG_INLINE', 'HTML to Image Inline'),
    ('PDF', 'PDF'),
    ('IMG_TO_PDF', 'Image to PDF'),
    ('HTML_TO_PDF', 'HTML to PDF'),
    ('HTML_TO_IMG_TO_PDF', 'HTML to Image to PDF'),
    ('ONLY_IMG', 'Image as Content'),
}

class Permission(models.Model):
    name = models.CharField(max_length=255, choices=PERMISSION_MAP)

    def __str__(self):
        return self.name

class SoftwarePermissions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='software_permissions')
    permissions = models.ManyToManyField(Permission, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user_permission')
        ]

    def __str__(self):
        return f"Permissions for {self.user.username}"

class Credentials(models.Model):
    credentials = models.FileField(upload_to='credentials/')  # Store file in the 'credentials' folder

    def __str__(self):
        return f"Credentials {self.id}"

class SMTPConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    SMTP_SECURITY_CHOICES = [
        (False, 'Non-SSL/TLS (Default Port 587)'),
        (True, 'SSL/TLS (Port 465)')
    ]

    host = models.CharField(max_length=255, help_text="SMTP host, e.g., 'smtp.example.com'")
    port = models.PositiveIntegerField(default=587, help_text="SMTP port, e.g., 587 for TLS or 465 for SSL")
    secure = models.BooleanField(
        choices=SMTP_SECURITY_CHOICES,
        default=False,
        help_text="True for SSL/TLS (Port 465), False for non-SSL/TLS (Port 587)"
    )
    auth_user = models.EmailField(help_text="Email address used for SMTP authentication")
    auth_password = models.CharField(max_length=128, help_text="Password for the SMTP authentication email")

    def __str__(self):
        return f"{self.auth_user} ({self.host}:{self.port})"

class EmailAccounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=255, default="")
    google_token = models.CharField(max_length=500, blank=True, null=True)
    credentials = models.TextField(null=True,blank=True)
    expiry_time = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if google_token is being set or updated
        if self.google_token:
            self.expiry_time = now() + timedelta(days=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Email Account"
        verbose_name_plural = "Email Accounts"


class AudienceData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50, default="First Campaign")
    email = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Audience Data"
        verbose_name_plural = "Audiences"

class Tags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=50, default="")

    def save(self, *args, **kwargs):
        # Prepend '{custom_}' to tag_name if not already added
        if not self.tag_name.startswith("{custom_}"):
            self.tag_name = f"{{custom_{self.tag_name}}}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = "Custom tag"
        verbose_name_plural = "Custom tags"

class tags_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    data = models.CharField(max_length=500, default="")

    def __str__(self):
        return f'{self.tag.tag_name}-{self.data}'

    class Meta:
        verbose_name = "Custom tag data"
        verbose_name_plural = "Custom tags Data"


class Messages(models.Model):
    FORMAT_CHOICES = [
        ('HTML', 'HTML Message Only'),
        ('HTML_IMG', 'HTML with Image Attachment'),
        ('ONLY_IMG', 'Image as Content'),
        ('HTML_TO_IMG', 'HTML to Image Conversion'),
        ('HTML_IMG_INLINE', 'HTML to Image Inline'),
        ('PDF', 'PDF Attachment'),
        ('IMG_TO_PDF', 'Image to PDF Conversion'),
        ('HTML_TO_PDF', 'HTML to PDF Conversion'),
        ('HTML_TO_IMG_TO_PDF', 'HTML to Image to PDF'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, default='')
    content = models.TextField(default='', blank=True, null=True)
    format_type = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='HTML')
    attachment_content = models.TextField(default='', blank=True, null=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)  # To handle file attachments like images or PDFs
    file_name = models.CharField(max_length=150, default='file')
    sender_name = models.CharField(max_length=150, default="{randomName}")
    unsuscribe_url = models.CharField(max_length=150, default="mailto:{receiverEmail}")

    def clean(self):
        # Validation for format_type
        if self.format_type == 'HTML' and (not self.subject or not self.content):
            raise ValidationError("Subject and content are required for HTML format.")

        if self.format_type == 'HTML_IMG' and (not self.content or not self.attachment):
            raise ValidationError("HTML content and an image attachment are required for HTML_IMG format.")
        
        if self.format_type == 'ONLY_IMG' and (not self.attachment):
            raise ValidationError("Image attachment is required for ONLY_IMG format.")
        
        if self.format_type == 'ONLY_IMG' and self.attachment and not self.attachment.name.lower().endswith(('png', 'jpg', 'jpeg')):
            raise ValidationError("Attachment must be an image file for ONLY_IMG format.")

        if self.format_type == 'HTML_IMG' and self.attachment and not self.attachment.name.lower().endswith(('png', 'jpg', 'jpeg')):
            raise ValidationError("Attachment must be an image file for HTML_IMG format.")
        
        if self.format_type == 'HTML_TO_IMG' and (not self.content or not self.attachment_content):
            raise ValidationError("HTML content and an image attachment content are required for HTML_TO_IMG format.")
        
        if self.format_type == 'HTML_IMG_INLINE' and (not self.attachment_content):
            raise ValidationError("HTML image attachment content are required for HTML_IMG_INLINE format.")
        
        if self.format_type == 'PDF' and not self.attachment:
            raise ValidationError("A PDF attachment is required for PDF format.")
        
        if self.format_type == 'PDF' and self.attachment and not self.attachment.name.lower().endswith('pdf'):
            raise ValidationError("Attachment must be a PDF file for PDF format.")
        
        if self.format_type == 'IMG_TO_PDF' and self.attachment and not self.attachment.name.lower().endswith(('png', 'jpg', 'jpeg')):
            raise ValidationError("Attachment must be an image file for IMG_TO_PDF format.")

        if self.format_type == 'HTML_TO_IMG_TO_PDF' and (not self.content or not self.attachment_content):
            raise ValidationError("HTML content and an image attachment content are required for HTML_TO_IMG_TO_PDF format.")
        
        if self.format_type == 'HTML_TO_PDF' and (not self.content or not self.attachment_content):
            raise ValidationError("HTML content and an PDF attachment content are required for HTML_TO_PDF format.")
        
    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        permissions = [
            ("can_use_html", "Can use HTML Message Only"),
            ("can_use_html_img", "Can use HTML with Image Attachment"),
            ("can_use_html_to_img", "Can use HTML to Image Conversion"),
            ("can_use_pdf", "Can use PDF Attachment"),
            ("can_use_img_to_pdf", "Can use Image to PDF Conversion"),
            ("can_use_html_to_pdf", "Can use HTML to PDF Conversion"),
            ("can_use_html_to_img_to_pdf", "Can use HTML to Image to PDF Conversion"),
        ]

sending_choices = [
        ('inbox', 'inbox'),
        ('draft', 'draft'),
    ]

class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=status_choices, max_length=12, default="created")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)
    audience_data = models.CharField(max_length=255, default="Target")  # New field
    send_from = models.CharField(choices=[
        ('API', 'API'),
        ('SMTP', 'SMTP'),
    ], max_length=10, default='API')  # New field


    def __str__(self):
        return f'{self.user.username.upper()} started a Campaign at Machine IP Address: {self.ip_address} at {self.date_time}.'

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"


class SiteSettings(models.Model):
    icon = models.ImageField(upload_to='site_icons/', verbose_name="Site Icon")
    login_image = models.ImageField(upload_to='site_icons/', verbose_name="Login Image",null=True,blank=True)

    def __str__(self):
        return f"Icon {self.id}"
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
