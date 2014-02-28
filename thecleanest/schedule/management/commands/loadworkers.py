from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from thecleanest.notifications.email import disaster
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
                if record['avatar_url']:
                    if worker.avatar_url != record['avatar_url']:
                        worker.avatar_url = record['avatar_url']
                        worker.save()

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
        workers_to_deactivate = NamelessWorker.objects.filter(is_active=True).exclude(email__in=emails)
        worker_count = workers_to_deactivate.count()
        if worker_count > 2:
            disaster('%i workers will soon be deactivated. This seems like too many.' % worker_count)
        else:
            for worker in workers_to_deactivate:
                worker.deactivate()
