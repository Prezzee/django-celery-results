"""Result Task Admin interface."""
from __future__ import absolute_import, unicode_literals

from celery.states import FAILURE
from django.contrib import admin, messages

from .models import TaskResult


class TaskResultAdmin(admin.ModelAdmin):
    """Admin-interface for results of tasks."""

    model = TaskResult
    list_display = ('task_id', 'task_name', 'date_done', 'status')
    list_filter = ('status', 'date_done')
    readonly_fields = ('task_args', 'task_kwargs', 'date_done', 'traceback', 'result', 'hidden', 'meta')
    search_fields = ('task_id', 'task_name')
    fieldsets = (
        (None, {
            'fields': (
                'task_id',
                'status',
                'content_type',
                'content_encoding',
            ),
            'classes': ('extrapretty', 'wide')
        }),
        ('Invocation', {
            'fields': (
                'task_name',
                'task_args',
                'task_kwargs',
            )
        }),
        ('Result', {
            'fields': (
                'result',
                'date_done',
                'traceback',
                'hidden',
                'meta',
            ),
            'classes': ('extrapretty', 'wide')
        }),
    )
    actions = ('resubmit_task',)
    change_actions = ('resubmit_task',)

    def resubmit_task(self, request, queryset):
        for task_result in queryset:
            if not task_result.status == FAILURE:
                messages.warning(request, 'Task ID {}: can only resubmit failed tasks, current status is {}'.format(task_result.task_id, task_result.status))

            else:
                try:
                    task_result.resubmit()
                    messages.success(request, 'Task ID {}: resubmitted successfully'.format(task_result.task_id))

                except Exception as e:
                    messages.error(request, str(e))

    resubmit_task.short_description = "Resubmit task(s) to the queue"


admin.site.register(TaskResult, TaskResultAdmin)
