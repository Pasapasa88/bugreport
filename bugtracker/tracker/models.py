from django.db import models
from django.utils import timezone

class Task(models.Model):
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Open')

    def __str__(self):
        return self.subject

    def last_comment_date(self):
        last_comment = self.comments.order_by('-created_at').first()
        return last_comment.created_at if last_comment else None

    def last_comment_annotation(self):
        last_comment = self.comments.order_by('-created_at').first()
        return last_comment.body[:100] + '...' if last_comment else ''


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    author = models.CharField(max_length=100, default='Anonymous')

    def __str__(self):
        return f'Comment on {self.task.subject}'
