from django import forms
from django.contrib.auth.models import User
from .models import Member, MemberRelationship

class UserCreationForm(forms.ModelForm):
    sponsor = forms.ModelChoiceField(queryset=Member.objects.all(), required=False, label='Sponsor')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['sponsor'].label_from_instance = lambda obj: obj.user.username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            sponsor = self.cleaned_data.get('sponsor')
            if sponsor:
                Member.objects.create(user=user, sponsor=sponsor)
        return user

class MemberRelationshipForm(forms.ModelForm):
    class Meta:
        model = MemberRelationship
        fields = ['parent', 'child']
    
    def __init__(self, *args, **kwargs):
        super(MemberRelationshipForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Member.objects.all()
        self.fields['child'].queryset = Member.objects.all()
        self.fields['parent'].label_from_instance = lambda obj: f"{obj.user.username}"
        self.fields['child'].label_from_instance = lambda obj: f"{obj.user.username}"
        
    def get_selected_ids(self):
            if self.is_valid():
                parent_id = self.cleaned_data['parent'].id
                child_id = self.cleaned_data['child'].id
                return parent_id, child_id
            else:
                return None, None