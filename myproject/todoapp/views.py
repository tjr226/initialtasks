# auto from django
from django.shortcuts import render, redirect, get_object_or_404

# copied from django-boards
from django.http import HttpResponse
from .models import TaskItem
from .forms import NewTaskItemForm, CompleteTaskButton, PushTaskButton, HideTaskButton, UnhideAllTasksButton
from datetime import datetime, timedelta


def home(request):
    new_task_form = NewTaskItemForm()
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
            new_task_task = TaskItem.objects.create(
                task_text=incoming_task_text)
            return redirect('home')
        elif 'unhide' in request.POST:
            items_to_unhide = TaskItem.objects
            items_to_unhide.update(hidden_boolean=False)
        #next section switches hidden_boolean to true
        elif 'hide' in request.POST:
            form = HideTaskButton(request.POST)
            if form.is_valid():
                form_item_id = request.POST['item_id']
                task_to_update = TaskItem.objects.get(id=form_item_id)
                task_to_update.hidden_boolean = True
                task_to_update.save()
            return redirect('home')
        #next section changes the next_update_date by adding the input from the field
        elif 'push' in request.POST:
            form = PushTaskButton(request.POST)
            if form.is_valid():
                form_item_id = request.POST['item_id']
                days_to_push = request.POST['days_to_push']
                task_to_update = TaskItem.objects.get(id=form_item_id)
                task_to_update.next_update_date = datetime.now() + timedelta(days=int(days_to_push))
                task_to_update.save()

            return redirect('home')
        
        # this section flips the completed boolean
        elif 'complete' in request.POST:
            form = CompleteTaskButton(request.POST)
            if form.is_valid():
                form_item_id = request.POST['item_id']
                task_to_update = TaskItem.objects.get(id=form_item_id)
                task_to_update.completed_boolean = True
                task_to_update.save()

            return redirect('home')
    else:
        new_task_form = NewTaskItemForm()
        complete_task_button = CompleteTaskButton()
        push_task_button = PushTaskButton()
        hidden_task_button = HideTaskButton()
        unhide_all_tasks_button = UnhideAllTasksButton()
        


    
    # first grab all Tasks that are not complete or hidden. then sort them by next_update_date
    items_to_render = TaskItem.objects.exclude(completed_boolean=True).exclude(hidden_boolean=True)
    items_to_render = items.order_by('next_update_date')

    

    return render(request, 'home.html', {
        'items': items_to_render,
        'new_task_form': new_task_form,
        'push_task_button': push_task_button,
        'complete_task_button': complete_task_button,
        'hidden_task_button': hidden_task_button,
        'unhide_all_tasks_button': unhide_all_tasks_button
    })
