from django.core.management.base import NoArgsCommand, CommandError
from thecleanest.schedule.models import NamelessWorker
import csv
import sys

class Command(NoArgsCommand):
    help = 'Load nameless workers from a CSV piped to stdin'

    def handle_noargs(self, **options):

        for record in csv.DictReader(sys.stdin):

            try:

                NamelessWorker.objects.get(email=record['email'])

            except NamelessWorker.DoesNotExist:

                NamelessWorker.objects.create(
                    first_name=record['first_name'],
                    last_name=record['last_name'],
                    email=record['email'],
                    avatar_url=record['avatar_url'],
                    is_active=True,
                )