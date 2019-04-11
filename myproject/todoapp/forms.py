from django import forms
from .models import TaskItem

class NewTaskItemForm(forms.ModelForm):
    # task = forms.CharField(widget=forms.Textarea(), max_length=4000)

    class Meta:
        model = TaskItem
        # next line picks out the tickler_text field from the TicklerItem model
        fields = ['task_text']

class CompleteTaskButton(forms.ModelForm):
    class Meta:
        model = TaskItem
        fields = []
        
class PushTaskButton(forms.ModelForm):
    class Meta:
        model = TaskItem
        fields = [] 

class HideTaskButton(forms.ModelForm):
    class Meta:
        model = TaskItem
        fields = []

class UnhideAllTasksButton(forms.ModelForm):
    class Meta:
        model = TaskItem
        fields = []