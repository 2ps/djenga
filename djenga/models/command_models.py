
from django.db import models


__all__ = [
    'ManagementCommand',
    'CommandOutput',
]


class ManagementCommand(models.Model):
    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        db_index=True,
        help_text='The full path of the command',
    )
    status = models.CharField(
        max_length=32,
        null=False,
        blank=False,
        help_text='The current status of the command',
    )
    last_run = models.DateTimeField(
        null=True,
        help_text='The last time this command was run',
    )
    last_success = models.DateTimeField(
        null=True,
        help_text='The last time this command was run successfully',
    )
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)


class CommandOutput(models.Model):
    command = models.ForeignKey(ManagementCommand)
    output = models.TextField(null=True)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    updated_at = models.DateTimeField(null=False, auto_now=True)
