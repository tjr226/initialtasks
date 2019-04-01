from django.db import models
from django.contrib.auth.models import User

class TicklerItem(models.Model):
    
    # contains
    # -tickler_text (text of the item)
    # -created_by   (user that created it)
    # -next_update_date (ideally will be the next date that the tickler item should bubble up to inbox)

    tickler_text = models.TextField(max_length=4000)
    # created_by = models.ForeignKey(User, related_name='tickler_items', on_delete='CASCADE')
    next_update_date = models.DateTimeField(auto_now_add=True)
    completed_boolean = models.BooleanField(default=False)

    def __str__(self):
        return self.tickler_text