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
        
class PushTaskButtonDays(forms.ModelForm):
    # button to push tasks into the future
    class Meta:
        model = TaskModel
        fields = [] 

class PushTaskButtonHours(forms.ModelForm):
    # button to push tasks into the future
    class Meta:
        model = TaskModel
        fields = [] 

class HideTaskButton(forms.ModelForm):
    # button to hide individual tasks
    class Meta:
        model = TaskModel
        fields = []

class ShowAllActiveTasksButton(forms.ModelForm):
    # button to unhide all tasks
    class Meta:
        model = TaskModel
        fields = []

class HideAllTasksButton(forms.ModelForm):
    # button to hide all tasks
    class Meta:
        model = TaskModel
        fields = []

class ShowNextFiveTasksButton(forms.ModelForm):
    # button to hide all tasks
    class Meta:
        model = TaskModel
        fields = []

class ShowAccomplishedTasksButton(forms.ModelForm):
    # button to hide all tasks
    class Meta:
        model = TaskModel
        fields = []
