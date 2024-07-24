from django.db import models
from ckeditor.fields import RichTextField
from simple_history.models import HistoricalRecords


class Reporter(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    priority = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    current_environment = models.CharField(max_length=50, choices=[
        ('not_started', 'Not Started'),
        ('dev', 'Dev/Local'),
        ('uat', 'UAT'),
        ('staging', 'Staging'),
        ('preprod', 'Preprod'),
        ('production', 'Production')
    ], default="not_started")
    start_date = models.DateField()
    expected_end_date = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('needs_review', 'Needs Review'),
        ('completed', 'Completed')
    ])
    end_date = models.DateField(blank=True, null=True)
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True)
    jira_ticket_link = models.URLField(blank=True, null=True)
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class TaskComments(models.Model):
    task = models.ForeignKey(Task, related_name='reports', on_delete=models.CASCADE)
    comment = RichTextField()
    attachments = models.FileField(upload_to='report_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "TaskComments"

    def __str__(self):
        return f"Report for {self.task.title}"

