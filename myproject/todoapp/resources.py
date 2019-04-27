from import_export import resources
from .models import TaskModel
from django.http import HttpResponse


class TaskResource(resources.ModelResource):
    class Meta:
        model = TaskModel


def export(request):
    task_resource = TaskResource()
    dataset = task_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response
