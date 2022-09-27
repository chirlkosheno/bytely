from django import forms


class UrlForm(forms.Form):
    full_url = forms.CharField(label='Url', max_length=1024)
