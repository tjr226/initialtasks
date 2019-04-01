# auto from django
from django.shortcuts import render, redirect

# copied from django-boards
from django.http import HttpResponse
from .models import TicklerItem
from .forms import NewTicklerItemForm


def home(request):
    new_task_form = NewTicklerItemForm(request.POST)


    # code to process form entries
    if request.method == 'POST':
        # code to absorb top form that creates new tasks
        if 'tickler_text' in request.POST:
            incoming_task_text = request.POST['tickler_text']
            new_tickler_task = TicklerItem.objects.create(tickler_text = incoming_task_text)
            return redirect('home')
        if 'completed_task' in request.POST:
            print("completed task button press")
            # to do
        if 'push' in request.POST:
            print("push task button press")
            #
    else:
        new_tickler_form = NewTicklerItemForm()

    items = TicklerItem.objects.exclude(completed_boolean=True)

    return render(request, 'home.html', {'items': items, 'form': new_tickler_form})
