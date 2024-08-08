from django.shortcuts import render, get_object_or_404
from .models import Task
from django.core.paginator import Paginator
from django.http import FileResponse,Http404
from django.conf import settings
import os



def task_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', 'created_at')
    sort_order = request.GET.get('sort_order', 'asc')
    order_prefix = '' if sort_order == 'asc' else '-'

    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(subject=query)

    tasks = tasks.order_by(f'{order_prefix}{sort_by}')

    paginator = Paginator(tasks, 20)
    page = request.GET.get('page')
    tasks_page = paginator.get_page(page)

    return render(request, 'tracker/task_list.html', {
        'tasks': tasks_page,
        'sort_by': sort_by,
        'sort_order': sort_order,
    })

def task_detail(request, task_id):
    task = get_object_or_404(Task, subject=task_id)
    comments = task.comments.order_by('-created_at')  # Комментарии в порядке убывания
    return render(request, 'tracker/task_detail.html', {'task': task, 'comments': comments})


def download_file(request, filename):
    file_path = os.path.join(rf'{settings.BASE_DIR}\tracker\attachments', filename)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        return response
    else:
        return Http404("File not found")