from django import forms
from .models import TaskModel

class NewTaskForm(forms.ModelForm):
    # form for new tasks

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
    # combined button to push tasks by hours and days
    class Meta:
        model = TaskModel
        fields = []


class PushTaskByWeekButton(forms.ModelForm):
    # push a task by one week
    class Meta:
        model = TaskModel
        fields = []


class PushTaskByMonthButton(forms.ModelForm):
    # push a task by one month
    class Meta:
        model = TaskModel
        fields = []

class PushTaskByYearButton(forms.ModelForm):
    #  push a task by a year
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
