from django.core.management.base import NoArgsCommand, CommandError
from thecleanest.schedule.generate import generate_schedule

class Command(NoArgsCommand):
    help = 'Generate kitchen duty schedule'

    def handle_noargs(self, **options):
        generate_schedule()
