from django import forms
from .models import TicklerItem

class NewTicklerItemForm(forms.ModelForm):
    # task = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = TicklerItem
        # next line picks out the tickler_text field from the TicklerItem model
        fields = ['tickler_text']

class CompleteTaskButton(forms.ModelForm):
    class Meta:
        model = TicklerItem
        fields = []
        
class PushTaskButton(forms.ModelForm):
    class Meta:
        model = TicklerItem
        fields = [] 