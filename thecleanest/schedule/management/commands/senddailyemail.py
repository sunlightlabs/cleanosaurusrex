from django.core.management.base import NoArgsCommand, CommandError
from thecleanest.schedule.models import Assignment
from thecleanest.notifications.email import assignment_today, assignment_next_week
from datetime import date, timedelta

class Command(NoArgsCommand):
    help = 'Sends the daily reminder email'

    def handle_noargs(self, **options):
        
        today = date.today()
        next_week = today + timedelta(days=7)
        
        # notify today's person
        
        try:
            assignment = Assignment.objects.get(date=today)
            assignment_today(assignment)
        except Assignment.DoesNotExist:
            pass # no assignment today
        
        # notify for next week
        
        try:
            assignment = Assignment.objects.get(date=next_week)
            assignment_next_week(assignment)
        except Assignment.DoesNotExist:
            pass # no assignment next week
