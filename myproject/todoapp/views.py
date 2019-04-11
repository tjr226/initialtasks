# auto from django
from django.shortcuts import render, redirect, get_object_or_404

# copied from django-boards
from django.http import HttpResponse
from .models import TaskModel
from .forms import NewTaskForm, CompleteTaskButton, PushTaskButton, HideTaskButton, UnhideAllTasksButton
from datetime import datetime, timedelta

def home(request):
    # create vars for all Django forms from forms.py
    # these are needed for the return render() function at the end of this home() function
    new_task_form = NewTaskForm()
    complete_task_button = CompleteTaskButton()
    push_task_button = PushTaskButton()
    hidden_task_button = HideTaskButton()
    unhide_all_tasks_button = UnhideAllTasksButton()

    # code to process form entries
    # buttons in Django are also form entries
    # each path redirects back to home, reloading the page
    if request.method == 'POST':

        # comments are below each IF/ELIF line
        if 'task_text' in request.POST:
            print(request.POST)
            # create a new task POST request
            # getting form text
            incoming_task_text = request.POST['task_text']
            days_to_push = request.POST['days_to_push']
            # new task created
            new_task = TaskModel.objects.create(task_text=incoming_task_text)
            # check incoming days_to_push
            days_to_push = int(days_to_push)
            if type(days_to_push) == type(int()):
                if days_to_push > 0:
                    new_task.next_update_date = datetime.now() + timedelta(days=int(days_to_push))
                    new_task.hidden_boolean = True
            new_task.save()
            return redirect('home')
        elif 'unhide' in request.POST:
            # unhide all tasks by setting hidden_boolean to False for all tasks
            tasks_to_unhide = TaskModel.objects
            tasks_to_unhide.update(hidden_boolean=False)
        elif 'hide' in request.POST:
            # hide individual task by setting hidden_boolean to True
            form = HideTaskButton(request.POST)
            if form.is_valid():
                form_task_id = request.POST['task_id']
                task_to_update = TaskModel.objects.get(id=form_task_id)
                task_to_update.hidden_boolean = True
                task_to_update.save()
            return redirect('home')
        elif 'push' in request.POST:
            # pushes tasks by adding the days_to_push form entry to the current date
            # also hides all pushed tasks
            form = PushTaskButton(request.POST)
            if form.is_valid():
                form_task_id = request.POST['task_id']
                days_to_push = request.POST['days_to_push']
                task_to_update = TaskModel.objects.get(id=form_task_id)
                # sets next_update_date by adding days_to_push to the current date
                task_to_update.next_update_date = datetime.now() + timedelta(days=int(days_to_push))
                # hides task
                task_to_update.hidden_boolean = True
                task_to_update.save()

            return redirect('home')
        elif 'complete' in request.POST:
            # completes tasks by setting Completed boolean to True
            form = CompleteTaskButton(request.POST)
            if form.is_valid():
                form_task_id = request.POST['task_id']
                task_to_update = TaskModel.objects.get(id=form_task_id)
                task_to_update.completed_boolean = True
                task_to_update.save()

            return redirect('home')

    # end IF statements to process POST requests

    # first grab all Tasks that are not complete or hidden. then sort them by next_update_date
    tasks_to_render = TaskModel.objects.exclude(completed_boolean=True).exclude(hidden_boolean=True)
    tasks_to_render = tasks_to_render.order_by('next_update_date')

    # render page using Django

    return render(request, 'home.html', {
        'tasks': tasks_to_render,
        'new_task_form': new_task_form,
        'push_task_button': push_task_button,
        'complete_task_button': complete_task_button,
        'hidden_task_button': hidden_task_button,
        'unhide_all_tasks_button': unhide_all_tasks_button
    })
