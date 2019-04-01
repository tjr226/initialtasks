# auto from django
from django.shortcuts import render, redirect

# copied from django-boards
from django.http import HttpResponse
from .models import TicklerItem
# from .forms import NewTicklerItemForm


def home(request):

    # code to create a new task
    if request.method == 'POST':
        incoming_task_text = request.POST['task']

        # add user stuff later
        # user = User.objects.first()

        new_tickler_task = TicklerItem.objects.create(
            tickler_text = incoming_task_text
        )

        return redirect('home')

    items = TicklerItem.objects.exclude(completed_boolean=True)

    return render(request, 'home.html', {'items': items})
