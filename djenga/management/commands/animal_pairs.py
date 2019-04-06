from argparse import ArgumentParser
from django.core.management.base import BaseCommand
from ...animal_pairs import animal_pair


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            '-n', '--count',
            dest='count',
            type=int,
            help='number of animal pairs to output',
            metavar='count',
            default=4,
        )

    def handle(self, count, *args, **options):  # pylint: disable=W0221
        for _ in range(count):
            self.stdout.write(animal_pair())
