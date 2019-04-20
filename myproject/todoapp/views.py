# auto from django
from django.shortcuts import render, redirect, get_object_or_404

# copied from django-boards
from django.http import HttpResponse
from .models import TaskModel
from .forms import NewTaskForm, CompleteTaskButton, PushTaskButton, HideTaskButton, UnhideAllTasksButton, HideAllTasksButton, ShowNextFiveTasksButton
from datetime import datetime, timedelta
from django.utils import timezone


def home(request):
    # create vars for all Django forms from forms.py
    # these are needed for the return render() function at the end of this home() function
    new_task_form = NewTaskForm()
    complete_task_button = CompleteTaskButton()
    push_task_button = PushTaskButton()
    hidden_task_button = HideTaskButton()
    unhide_all_tasks_button = UnhideAllTasksButton()
    hide_all_tasks_button = HideAllTasksButton()
    show_next_five_tasks_button = ShowNextFiveTasksButton()

    # code to process form entries
    # buttons in Django are also form entries
    # each path redirects back to home, reloading the page
    if request.method == 'POST':

        # comments are below each IF/ELIF line
        if 'task_text' in request.POST:

            # create a new task POST request
            # getting form text
            incoming_task_text = request.POST['task_text']
            days_to_push = request.POST['days_to_push']
            # new task created
            new_task = TaskModel.objects.create(task_text=incoming_task_text)

            # if no entry in days_to_push field, redirect home. no more action necessary
            if days_to_push == "":
                return redirect('home')

            # cast incoming days_to_push string to int
            days_to_push = int(days_to_push)
            if type(days_to_push) == type(int()):
                if days_to_push > 0:
                    new_task.next_update_date = datetime.now() + timedelta(days=int(days_to_push))
                    new_task.hidden_boolean = True
            new_task.save()
            return redirect('home')
        elif 'unhide_all' in request.POST:
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
        elif 'hide_all' in request.POST:
            print('hide all')
            form = HideAllTasksButton(request.POST)
            if form.is_valid():
                all_current_tasks = TaskModel.objects.exclude(completed_boolean=True)
                all_current_tasks.update(hidden_boolean=True)
            return redirect('home')

        elif 'show_next_five_tasks_button' in request.POST:
            print("show next five clicked")
            form = ShowNextFiveTasksButton(request.POST)
            if form.is_valid():
                all_tasks = TaskModel.objects.exclude(completed_boolean=True)
                
                all_tasks.update(hidden_boolean=False)
                # print(all_tasks)
                all_tasks = all_tasks.order_by('next_update_date')
                # print(all_tasks)
                tasks_to_render = all_tasks[:5]
                # print(tasks_to_render)

                TaskModel.objects.exclude(id__in=tasks_to_render).update(hidden_boolean=True)


                return render(request, 'home.html', {
                    'tasks': tasks_to_render,
                    'new_task_form': new_task_form,
                    'push_task_button': push_task_button,
                    'complete_task_button': complete_task_button,
                    'hidden_task_button': hidden_task_button,
                    'unhide_all_tasks_button': unhide_all_tasks_button,
                    'hide_all_tasks_button': hide_all_tasks_button,
                    'show_next_five_tasks_button': show_next_five_tasks_button,
                })

            else:
                redirect('home')




    # end IF statements to process POST requests

    # first grab all Tasks that are not complete or hidden. then sort them by next_update_date
    tasks_to_render = TaskModel.objects.exclude(
        completed_boolean=True).exclude(hidden_boolean=True)
    tasks_to_render = tasks_to_render.order_by('next_update_date')

    # render page using Django

    return render(request, 'home.html', {
        'tasks': tasks_to_render,
        'new_task_form': new_task_form,
        'push_task_button': push_task_button,
        'complete_task_button': complete_task_button,
        'hidden_task_button': hidden_task_button,
        'unhide_all_tasks_button': unhide_all_tasks_button,
        'hide_all_tasks_button': hide_all_tasks_button,
        'show_next_five_tasks_button': show_next_five_tasks_button,
    })
