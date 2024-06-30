from django import forms
from django.contrib.auth.models import User
from .models import Member

class UserCreationForm(forms.ModelForm):
    sponsor = forms.ModelChoiceField(queryset=Member.objects.all(), required=False, label='Sponsor')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            sponsor = self.cleaned_data.get('sponsor')
            if sponsor:
                Member.objects.create(user=user, sponsor=sponsor)
        return user
