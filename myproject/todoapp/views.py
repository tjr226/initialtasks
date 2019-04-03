# auto from django
from django.shortcuts import render, redirect, get_object_or_404

# copied from django-boards
from django.http import HttpResponse
from .models import TicklerItem
from .forms import NewTicklerItemForm, DeleteTaskButton, PushTaskButton
from datetime import datetime, timedelta


def home(request):
    new_task_form = NewTicklerItemForm(request.POST)

    new_tickler_form = NewTicklerItemForm()
    delete_task_button = DeleteTaskButton()
    push_task_button = PushTaskButton()

    # code to process form entries
    if request.method == 'POST':
        # code to absorb top form that creates new tasks
        if 'tickler_text' in request.POST:
            incoming_task_text = request.POST['tickler_text']
            new_tickler_task = TicklerItem.objects.create(
                tickler_text=incoming_task_text)
            return redirect('home')
        elif 'push' in request.POST:
            print("push task button press")

            form = PushTaskButton(request.POST)
            if form.is_valid():
                x = request.POST['item_tickler_text']
                days_to_push = request.POST['days_to_push']
                tickler_to_update = TicklerItem.objects.get(tickler_text=x)
                tickler_to_update.next_update_date = datetime.now() + timedelta(days=int(days_to_push))
                tickler_to_update.save()

            return redirect('home')
            #
        elif 'delete' in request.POST:
            print("delete task button press")
            form = DeleteTaskButton(request.POST)
            if form.is_valid():
                x = request.POST['item_tickler_text']
                tickler_to_update = TicklerItem.objects.get(tickler_text=x)
                tickler_to_update.completed_boolean = True
                tickler_to_update.save()

            return redirect('home')
    else:
        new_tickler_form = NewTicklerItemForm()
        delete_task_button = DeleteTaskButton()
        push_task_button = PushTaskButton()

        # completed_task_button = CompleteTaskForm()
        # push_task_form = PushTaskForm()

    

    items = TicklerItem.objects.exclude(completed_boolean=True)
    items = items.order_by('next_update_date')

    

    return render(request, 'home.html', {
        'items': items,
        'new_tickler_form': new_tickler_form,
        'push_task_button': push_task_button,
        'delete_task_button': delete_task_button
    })
