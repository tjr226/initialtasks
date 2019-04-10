# auto from django
from django.shortcuts import render, redirect, get_object_or_404

# copied from django-boards
from django.http import HttpResponse
from .models import TicklerItem
from .forms import NewTicklerItemForm, CompleteTaskButton, PushTaskButton, HideTaskButton, UnhideAllTasksButton
from datetime import datetime, timedelta


def home(request):
    new_tickler_form = NewTicklerItemForm()
    complete_task_button = CompleteTaskButton()
    push_task_button = PushTaskButton()
    hidden_task_button = HideTaskButton()
    unhide_all_tasks_button = UnhideAllTasksButton()
                              

    # code to process form entries
    if request.method == 'POST':
        #first section of if/elif, creates a new tickler task
        if 'tickler_text' in request.POST:
            # I don't need to figure out IDs for incoming tasks because they don't have one yet
            incoming_task_text = request.POST['tickler_text']
            new_tickler_task = TicklerItem.objects.create(
                tickler_text=incoming_task_text)
            return redirect('home')
        elif 'unhide' in request.POST:
            items = TicklerItem.objects
            items.update(hidden_boolean=False)
        #next section switches hidden_boolean to true
        elif 'hide' in request.POST:
            form = HideTaskButton(request.POST)
            if form.is_valid():
                x = request.POST['item_id']
                tickler_to_update = TicklerItem.objects.get(id=x)
                tickler_to_update.hidden_boolean = True
                tickler_to_update.save()
            return redirect('home')
        #next section changes the next_update_date by adding the input from the field
        elif 'push' in request.POST:
            form = PushTaskButton(request.POST)
            if form.is_valid():
                x = request.POST['item_id']
                days_to_push = request.POST['days_to_push']
                tickler_to_update = TicklerItem.objects.get(id=x)
                tickler_to_update.next_update_date = datetime.now() + timedelta(days=int(days_to_push))
                tickler_to_update.save()

            return redirect('home')
        
        # this section flips the completed boolean
        elif 'complete' in request.POST:
            form = CompleteTaskButton(request.POST)
            if form.is_valid():
                x = request.POST['item_id']
                tickler_to_update = TicklerItem.objects.get(id=x)
                tickler_to_update.completed_boolean = True
                tickler_to_update.save()

            return redirect('home')
    else:
        new_tickler_form = NewTicklerItemForm()
        complete_task_button = CompleteTaskButton()
        push_task_button = PushTaskButton()
        hidden_task_button = HideTaskButton()
        unhide_all_tasks_button = UnhideAllTasksButton()
        


    

    items = TicklerItem.objects.exclude(completed_boolean=True).exclude(hidden_boolean=True)
    items = items.order_by('next_update_date')

    

    return render(request, 'home.html', {
        'items': items,
        'new_tickler_form': new_tickler_form,
        'push_task_button': push_task_button,
        'complete_task_button': complete_task_button,
        'hidden_task_button': hidden_task_button,
        'unhide_all_tasks_button': unhide_all_tasks_button
    })
