from django import forms
from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class GroupIdForm(forms.Form):
    group_id = forms.IntegerField(label='Group ID')