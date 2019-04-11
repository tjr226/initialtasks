from django import forms
from .models import TaskModel

class NewTaskForm(forms.ModelForm):

    class Meta:
        model = TaskModel
        # next line picks out the task_text field from the TaskModel
        fields = ['task_text']

class CompleteTaskButton(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = []
        
class PushTaskButton(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = [] 

class HideTaskButton(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = []

class UnhideAllTasksButton(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = []