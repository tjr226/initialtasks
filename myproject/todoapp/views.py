# auto from django
from django.shortcuts import render, redirect

# copied from django-boards
from .models import TaskModel, TaskModel.objects
from .forms import NewTaskForm, CompleteTaskButton, HideTaskButton, ShowAllActiveTasksButton, HideAllTasksButton, ShowNextFiveTasksButton, ShowAccomplishedTasksButton, PushTaskButton
from datetime import datetime, timedelta
from django.utils import timezone


def home(request):
    # create vars for all Django forms from forms.py
    # these are needed for the return render() function at the end of this home() function
    new_task_form = NewTaskForm()
    complete_task_button = CompleteTaskButton()
    push_task_button = PushTaskButton()
    hidden_task_button = HideTaskButton()
    show_all_active_tasks_button = ShowAllActiveTasksButton()
    hide_all_tasks_button = HideAllTasksButton()
    show_next_five_tasks_button = ShowNextFiveTasksButton()
    show_accomplished_tasks_button = ShowAccomplishedTasksButton()

    # code to process form entries
    # buttons in Django are also form entries
    # each path redirects back to home, reloading the page
    if request.method == 'POST':

        # comments are below each IF/ELIF line
        if 'task_text' in request.POST:

            # create a new task POST request
            # getting form text
            incoming_task_text = request.POST['task_text']
            incoming_task_why = request.POST['why']
            days_to_push = request.POST['days_to_push']
            # new task created
            new_task = TaskModel.objects.create(
                task_text=incoming_task_text, 
                why=incoming_task_why)
            print(new_task.why)
            print("printed task")
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
        elif 'show_all_active' in request.POST:
            # show all tasks by setting hidden_boolean to False for all tasks
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

        # elif 'push_hours' in request.POST:
        #         # pushes tasks by adding the days_to_push form entry to the current date
        #         # also hides all pushed tasks
        #     form = PushTaskButtonHours(request.POST)
        #     if form.is_valid():
        #         form_task_id = request.POST['task_id']
        #         hours_to_push = request.POST['hours_to_push']
        #         task_to_update = TaskModel.objects.get(id=form_task_id)
        #         # sets next_update_date by adding days_to_push to the current date
        #         task_to_update.next_update_date = datetime.now() + timedelta(hours=int(hours_to_push))
        #         # hides task
        #         task_to_update.hidden_boolean = True
        #         task_to_update.save()

        #     return redirect('home')

        # elif 'push_days' in request.POST:
        #     # pushes tasks by adding the days_to_push form entry to the current date
        #     # also hides all pushed tasks
        #     form = PushTaskButtonDays(request.POST)
        #     if form.is_valid():
        #         form_task_id = request.POST['task_id']
        #         days_to_push = request.POST['days_to_push']
        #         task_to_update = TaskModel.objects.get(id=form_task_id)
        #         # sets next_update_date by adding days_to_push to the current date
        #         task_to_update.next_update_date = datetime.now() + timedelta(days=int(days_to_push))
        #         # hides task
        #         task_to_update.hidden_boolean = True
        #         task_to_update.save()

        #     return redirect('home')
        elif 'push_task' in request.POST:
            form = PushTaskButton(request.POST)
            if form.is_valid():
                form_task_id = request.POST['task_id']
                hours_to_push = request.POST['hours_to_push']
                days_to_push = request.POST['days_to_push']
                task_to_update = TaskModel.objects.get(id=form_task_id)
                
                if len(hours_to_push) < 1:
                    hours_to_push = 0
                if len(days_to_push) < 1:
                    days_to_push = 0
            
                task_to_update.next_update_date = datetime.now() + timedelta(hours=int(hours_to_push)) + timedelta(days=int(days_to_push))
                task_to_update.hidden_boolean = True
                task_to_update.save()
            return redirect('home')

        elif 'complete_task_button' in request.POST:
            # completes tasks by setting Completed boolean to True
            form = CompleteTaskButton(request.POST)
            if form.is_valid():
                form_task_id = request.POST['task_id']
                task_to_update = TaskModel.objects.get(id=form_task_id)
                task_to_update.completed_boolean = True
                task_to_update.save()

            return redirect('home')
        elif 'hide_all' in request.POST:
            # this request sets the hidden_boolean of all active tasks to TRUE
            form = HideAllTasksButton(request.POST)
            if form.is_valid():
                all_current_tasks = TaskModel.objects.exclude(
                    completed_boolean=True)
                # update boolean for all active (not completed) tasks
                all_current_tasks.update(hidden_boolean=True)
            return redirect('home')

        elif 'show_next_five_tasks_button' in request.POST:
            # this request hides all tasks, then unhides the next 5.
            form = ShowNextFiveTasksButton(request.POST)
            if form.is_valid():
                # get all incomplete tasks
                all_tasks = TaskModel.objects.exclude(completed_boolean=True)
                # unhide all tasks (you want to see all of the next 5, even if they are hidden)
                all_tasks.update(hidden_boolean=False)
                # sort all active tasks by the next update date
                all_tasks = all_tasks.order_by('next_update_date')
                # slice all_tasks and grab the first five, these will be rendered
                tasks_to_render = all_tasks[:5]
                # go back and hide all other tasks, otherwise they will pop up again b/c they aren't hidden
                TaskModel.objects.exclude(
                    id__in=tasks_to_render).update(hidden_boolean=True)

                return render(request, 'home.html', {
                    'tasks': tasks_to_render,
                    'new_task_form': new_task_form,
                    'push_task_button': push_task_button,
                    'complete_task_button': complete_task_button,
                    'hidden_task_button': hidden_task_button,
                    'show_all_active_tasks_button': show_all_active_tasks_button,
                    'hide_all_tasks_button': hide_all_tasks_button,
                    'show_next_five_tasks_button': show_next_five_tasks_button,
                    'show_accomplished_tasks_button': show_accomplished_tasks_button,
                })

            else:
                redirect('home')

        elif 'show_accomplished_tasks_button' in request.POST:
            # this request hides all tasks, then unhides the next 5.
            form = ShowAccomplishedTasksButton(request.POST)
            if form.is_valid():
                # get all incomplete tasks
                accomplished_tasks = TaskModel.objects.exclude(
                    completed_boolean=False)
                # unhide all tasks (you want to see all of the next 5, even if they are hidden)
                accomplished_tasks = accomplished_tasks.order_by(
                    '-next_update_date')
                # slice all_tasks and grab the first five, these will be rendered

                return render(request, 'home.html', {
                    'tasks': accomplished_tasks,
                    'new_task_form': new_task_form,
                    'push_task_button': push_task_button,
                    'complete_task_button': complete_task_button,
                    'hidden_task_button': hidden_task_button,
                    'show_all_active_tasks_button': show_all_active_tasks_button,
                    'hide_all_tasks_button': hide_all_tasks_button,
                    'show_next_five_tasks_button': show_next_five_tasks_button,
                    'show_accomplished_tasks_button': show_accomplished_tasks_button,
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
        'show_all_active_tasks_button': show_all_active_tasks_button,
        'hide_all_tasks_button': hide_all_tasks_button,
        'show_next_five_tasks_button': show_next_five_tasks_button,
        'show_accomplished_tasks_button': show_accomplished_tasks_button,
    })
