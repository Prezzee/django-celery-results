"""Result Task Admin interface."""

from celery.states import FAILURE
from django.contrib import admin, messages

from django.conf import settings
from django.utils.translation import gettext_lazy as _

try:
    ALLOW_EDITS = settings.DJANGO_CELERY_RESULTS['ALLOW_EDITS']
except (AttributeError, KeyError):
    ALLOW_EDITS = False
    pass

from .models import TaskResult


class TaskResultAdmin(admin.ModelAdmin):
    """Admin-interface for results of tasks."""

    model = TaskResult
    date_hierarchy = 'date_done'
    list_display = ('task_id', 'task_name', 'date_done', 'status', 'worker')
    list_filter = ('status', 'date_done', 'task_name', 'worker')
    readonly_fields = ('date_created', 'date_done', 'result', 'meta')
    search_fields = ('task_name', 'task_id', 'status', 'task_args',
                     'task_kwargs')
    fieldsets = (
        (None, {
            'fields': (
                'task_id',
                'task_name',
                'status',
                'worker',
                'content_type',
                'content_encoding',
            ),
            'classes': ('extrapretty', 'wide')
        }),
        (_('Parameters'), {
            'fields': (
                'task_args',
                'task_kwargs',
            ),
            'classes': ('extrapretty', 'wide')
        }),
        (_('Result'), {
            'fields': (
                'result',
                'date_created',
                'date_done',
                'traceback',
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

            try:
                task_result.resubmit()
                messages.success(request, 'Task ID {}: resubmitted successfully'.format(task_result.task_id))

            except Exception as e:
                messages.error(request, str(e))

    resubmit_task.short_description = "Resubmit task(s) to the queue"

    def get_readonly_fields(self, request, obj=None):
        if ALLOW_EDITS:
            return self.readonly_fields
        else:
            return list(set(
                [field.name for field in self.opts.local_fields]
            ))


admin.site.register(TaskResult, TaskResultAdmin)
