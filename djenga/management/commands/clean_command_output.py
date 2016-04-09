
from djenga.management.commands import StatusCommand
from djenga.models import ManagementCommand
from djenga.models import CommandOutput


class Command(StatusCommand):
    help = 'Cleans up the djenga.models.CommandOutput values by removing old entries'

    def __init__(self):
        super(Command, self).__init__()
        self.commands = []
        self.keep = None

    def add_arguments(self, parser):
        parser.add_argument(
            '-n', '--keep',
            help='Saves the last N runs of the command and delete the rest',
            type=int,
            default=10,
            dest='keep')

    def load_commands(self):
        self.commands = ManagementCommand.objects.all()

    def clean_command(self, command_id):
        rg_ids = list(CommandOutput.objects.filter(
            command_id=command_id
        ).order_by('-id').values_list('id', flat=True))
        if rg_ids and len(rg_ids) > self.keep:
            rg_ids = rg_ids[self.keep:]
            CommandOutput.objects.filter(
                id__in=rg_ids
            ).delete()

    def clean_commands(self):
        for x in self.commands:
            self.plain_log('Cleaning ')
            self.color_log(self.style.SQL_TABLE, x.name)
            self.plain_log('...')
            self.clean_command(x.id)
            self.color_log(self.style.SUCCESS, 'Done.\n')

    def handle(self, keep, *args, **options):
        self.keep = keep
        self.load_commands()
        self.clean_commands()
        return ''
