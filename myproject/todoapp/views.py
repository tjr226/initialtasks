# auto from django
from django.shortcuts import render, redirect

# copied from django-boards
from django.http import HttpResponse
from .models import TicklerItem
# from .forms import NewTicklerItemForm


def home(request):

    # code to process form entries
    if request.method == 'POST':
        # code to absorb top form that creates new tasks
        if 'new_task' in request.POST:
            incoming_task_text = request.POST['new_task']
            new_tickler_task = TicklerItem.objects.create(tickler_text = incoming_task_text)
            return redirect('home')
        if 'completed_task' in request.POST:
            print("completed task button press")
            # to do
        if 'push' in request.POST:
            print("push task button press")
            #

    items = TicklerItem.objects.exclude(completed_boolean=True)

    return render(request, 'home.html', {'items': items})
