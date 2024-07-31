from django.shortcuts import render, get_object_or_404
from .models import Task
from django.core.paginator import Paginator


def task_list(request):
    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(id=query)
    else:
        tasks = Task.objects.all()

    paginator = Paginator(tasks, 20)  # Ограничение до 20 заявок на странице
    page = request.GET.get('page')
    tasks_page = paginator.get_page(page)

    return render(request, 'tracker/task_list.html', {'tasks': tasks_page})


def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    comments = task.comments.order_by('-created_at')  # Комментарии в порядке убывания
    return render(request, 'tracker/task_detail.html', {'task': task, 'comments': comments})
