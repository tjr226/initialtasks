from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class TaskModel(models.Model):
    
    # text of todo
    task_text = models.TextField(max_length=4000)

    # why
    why = models.TextField(
        max_length=400,
        default=""
        )

    # next date it will come up in the system
    next_update_date = models.DateTimeField(auto_now_add=True)

    # completed or not
    completed_boolean = models.BooleanField(default=False)

    # hidden or not
    hidden_boolean = models.BooleanField(default=False)

    def __str__(self):
        return self.task_text