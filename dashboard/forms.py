from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
    username = forms.CharField(label="Username or Email",max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class EmailAccountsForm(forms.ModelForm):
    class Meta:
        model = EmailAccounts
        fields = ['email', 'password','credentials']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
            'credentials': forms.Textarea(attrs={'placeholder': 'Enter Credentials'}),
        }

class AudienceDataForm(forms.ModelForm):
    class Meta:
        model = AudienceData
        fields = ['email', 'tag']

class BulkUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV File",
        widget=forms.FileInput(attrs={'accept': '.csv'}),
    )


class EmailAccountsBulkUploadForm(forms.Form):
    csv_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Upload'))

class AudienceBulkUploadForm(forms.Form):
    csv_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Upload'))


class SingleMessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['subject', 'content','format_type','attachment', 'file_name', 'sender_name', 'unsuscribe_url', 'attachment_content']

class EditMessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['subject', 'content', 'format_type', 'file_name', 'sender_name', 'unsuscribe_url', 'attachment_content', 'attachment']

class BulkDataUploadForm(forms.Form):
    tag = forms.CharField()
    csv_file = forms.FileField()

class BulkMessageUploadForm(forms.Form):
    csv_file = forms.FileField()

class TagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['tag_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        tag = super().save(commit=False)
        if self.user:
            tag.user = self.user
        if commit:
            tag.save()
        return tag

class BulkUploadForm(forms.Form):
    tag = forms.ModelChoiceField(queryset=Tags.objects.none(), label="Select Tag")
    file = forms.FileField(label="Upload CSV File")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['tag'].queryset = Tags.objects.filter(user=self.user)

class CampaignForm(forms.ModelForm):
    # Use a CharField to select tags instead of emails
    audience_data = forms.ChoiceField(choices=[], label="Select Audience Data")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            # Fetch distinct tags based on the user
            unique_tags = AudienceData.objects.filter(user=self.user).values_list('tag', flat=True).distinct()
            self.fields['audience_data'].choices = [(tag, tag) for tag in unique_tags]

        # if self.instance and self.instance.audience_data:
        #     self.initial['audience_data'] = self.instance.audience_data.tag  # Set initial tag if exists

    class Meta:
        model = Campaign
        fields = ['ip_address', 'audience_data', 'send_from']
        widgets = {
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'send_from': forms.Select(attrs={'class': 'form-control'}),
        }


class SMTPConfigurationForm(forms.ModelForm):
    class Meta:
        model = SMTPConfiguration
        fields = ['host', 'port', 'secure', 'auth_user', 'auth_password']