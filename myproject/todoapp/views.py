# auto from django
from django.shortcuts import render, redirect, get_object_or_404

# copied from django-boards
from django.http import HttpResponse
from .models import TaskModel
from .forms import NewTaskForm, CompleteTaskButton, PushTaskButton, HideTaskButton, UnhideAllTasksButton
from datetime import datetime, timedelta


def home(request):
    new_task_form = NewTaskForm()
    complete_task_button = CompleteTaskButton()
    push_task_button = PushTaskButton()
    hidden_task_button = HideTaskButton()
    unhide_all_tasks_button = UnhideAllTasksButton()
                              

    # code to process form entries
    if request.method == 'POST':
        #first section of if/elif, creates a new task
        if 'task_text' in request.POST:
            # I don't need to figure out IDs for incoming tasks because they don't have one yet
            incoming_task_text = request.POST['task_text']
            new_task_task = TaskModel.objects.create(
                task_text=incoming_task_text)
            return redirect('home')
        elif 'unhide' in request.POST:
            tasks_to_unhide = TaskModel.objects
            tasks_to_unhide.update(hidden_boolean=False)
        #next section switches hidden_boolean to true
        elif 'hide' in request.POST:
            form = HideTaskButton(request.POST)
            if form.is_valid():
                form_task_id = request.POST['task_id']
                task_to_update = TaskModel.objects.get(id=form_task_id)
                task_to_update.hidden_boolean = True
                task_to_update.save()
            return redirect('home')
        #next section changes the next_update_date by adding the input from the field
        elif 'push' in request.POST:
            form = PushTaskButton(request.POST)
            if form.is_valid():
                form_task_id = request.POST['task_id']
                days_to_push = request.POST['days_to_push']
                task_to_update = TaskModel.objects.get(id=form_task_id)
                task_to_update.next_update_date = datetime.now() + timedelta(days=int(days_to_push))
                task_to_update.hidden_boolean = True
                task_to_update.save()

            return redirect('home')
        
        # this section flips the completed boolean
        elif 'complete' in request.POST:
            form = CompleteTaskButton(request.POST)
            if form.is_valid():
                form_task_id = request.POST['task_id']
                task_to_update = TaskModel.objects.get(id=form_task_id)
                task_to_update.completed_boolean = True
                task_to_update.save()

            return redirect('home')

    # end IF statement to process POST requests
    
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
