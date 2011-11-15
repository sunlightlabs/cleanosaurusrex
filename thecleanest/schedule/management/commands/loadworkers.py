from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from thecleanest.schedule.models import NamelessWorker
import csv
import sys

class Command(NoArgsCommand):
    help = 'Load nameless workers from a CSV piped to stdin'

    def handle_noargs(self, **options):

        excused = getattr(settings, 'EXCUSED', [])
        emails = []

        for record in csv.DictReader(sys.stdin):

            emails.append(record['email'])

            try:

                worker = NamelessWorker.objects.get(email=record['email'])

            except NamelessWorker.DoesNotExist:

                worker = NamelessWorker.objects.create(
                    first_name=record['first_name'],
                    last_name=record['last_name'],
                    email=record['email'],
                    avatar_url=record['avatar_url'],
                )

            worker.is_active = record['email'] not in excused
            worker.save()

        # deactivate anyone that was not in the incoming use list
        NamelessWorker.objects.exclude(email__in=emails).update(is_active=False)