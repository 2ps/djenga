
from djenga.management.commands import StatusCommand


class Command(StatusCommand):
    def handle(self, *args, **options):
        self.debug('Hello Sesame')
        self.info('Hello Stella')
        self.warning('Hello Penny')
        return ''

