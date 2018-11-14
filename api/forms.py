from django.contrib.auth.models import User
from django import forms
from .models import Posts

class EntryForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = '__all__'

    def clean_author(self):
        if not self.cleaned_data['author']:
            return User()
        return self.cleaned_data['author']

    def clean_last_modified_by(self):
        if not self.cleaned_data['last_modified_by']:
            return User()
        return self.cleaned_data['last_modified_by']
