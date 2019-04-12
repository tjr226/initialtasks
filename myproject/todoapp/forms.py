from django import forms
from .models import TaskModel

class NewTaskForm(forms.ModelForm):
    # form for new tasks
    days_to_push = forms.IntegerField(required=False)
    class Meta:
        model = TaskModel
        # next line picks out the task_text field from the TaskModel
        fields = ['task_text']

class CompleteTaskButton(forms.ModelForm):
    # button to complete tasks
    class Meta:
        model = TaskModel
        fields = []
        
class PushTaskButton(forms.ModelForm):
    # button to push tasks into the future
    class Meta:
        model = TaskModel
        fields = [] 

class HideTaskButton(forms.ModelForm):
    # button to hide individual tasks
    class Meta:
        model = TaskModel
        fields = []

class UnhideAllTasksButton(forms.ModelForm):
    # button to unhide all tasks
    class Meta:
        model = TaskModel
        fields = []

class UnhideTodayTasksButton(forms.ModelForm):
    # button to unhide tasks dated 24hrs from now or less
    class Meta:
        model = TaskModel
        fields = []