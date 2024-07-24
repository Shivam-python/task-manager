from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Task, TaskComments, Reporter, Project
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.safestring import mark_safe


class TaskAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Task
        fields = '__all__'


class TaskCommentsAdminForm(forms.ModelForm):
    comment = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = TaskComments
        fields = '__all__'


class TaskCommentsInline(admin.TabularInline):
    model = TaskComments
    form = TaskCommentsAdminForm
    extra = 1

    readonly_fields = ('rendered_comment', 'created_at', 'attachments')

    def rendered_comment(self, obj):
        return mark_safe(obj.comment)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This means the task object is being edited, not created
            return self.readonly_fields + ('comment',)
        return ()

    def has_change_permission(self, request, obj=None):
        if obj:  # This means the task object is being edited, not created
            return False
        return super().has_change_permission(request, obj)

    rendered_comment.short_description = 'Comment'


@admin.register(Task)
class TaskAdmin(SimpleHistoryAdmin):
    form = TaskAdminForm
    list_display = ('title', 'priority', 'start_date', 'expected_end_date', 'status', 'reporter')
    search_fields = ('title', 'reporter__name')
    inlines = [TaskCommentsInline]


@admin.register(TaskComments)
class TaskCommentsAdmin(admin.ModelAdmin):
    form = TaskCommentsAdminForm
    list_display = ('task', 'created_at')
    search_fields = ('task__title',)


@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


# Register the historical model to the admin site
admin.site.register(Task.history.model, SimpleHistoryAdmin)
