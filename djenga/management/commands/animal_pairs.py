from argparse import ArgumentParser
from django.core.management.base import BaseCommand
from djenga.animal_pairs import animal_pair


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

    def handle(self, count, *args, **options):
        for x in range(count):
            self.stdout.write(animal_pair())
