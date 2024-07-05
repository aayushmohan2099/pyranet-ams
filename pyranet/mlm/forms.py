from django import forms
from django.contrib.auth.models import User
from .models import Member, MemberRelationship, Company, Product

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

class UpdateUserForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    sponsor = forms.ModelChoiceField(queryset=Member.objects.all(), required=False, label='Sponsor')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['sponsor'].label_from_instance = lambda obj: obj.user.username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            sponsor = self.cleaned_data.get('sponsor')
            if sponsor:
                # Update existing Member object if it exists
                member, created = Member.objects.get_or_create(user=user)
                member.sponsor = sponsor
                member.save()
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
            
class EditMemberRelationshipForm(forms.ModelForm):
    class Meta:
        model = MemberRelationship
        fields = ['parent', 'child']
    
    def __init__(self, *args, **kwargs):
        super(EditMemberRelationshipForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Member.objects.all()
        self.fields['child'].queryset = Member.objects.all()
        self.fields['parent'].label_from_instance = lambda obj: f"{obj.user.username}"
        self.fields['child'].label_from_instance = lambda obj: f"{obj.user.username}"

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'license_number', 'description', 'logo', 'base_profit_per_member', 'Products_offered']

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['Products_offered'].queryset = Product.objects.all()
        self.fields['Products_offered'].label_from_instance = lambda obj: f"{obj.name}"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']