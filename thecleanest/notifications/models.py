from django.db import models
from datetime import datetime, date
from thecleanest.schedule.models import NamelessWorker, Assignment
from thecleanest.notifications import email
from settings import NUDGE_GRACE_PERIOD

class Nudge(models.Model):
    target = models.ForeignKey(NamelessWorker,
                               related_name='nudges', null=False)
    timestamp = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return "%s nudged @ %s" % (unicode(self.target), unicode(self.timestamp))

    def save(self, *args, **kwargs):
        super(Nudge, self).save(*args, **kwargs)

        today = date.today()
        today_range = (datetime(today.year, today.month, today.day, 0, 0, 0),
                       datetime(today.year, today.month, today.day, 23, 59, 59))
        assignment = Assignment.objects.get(date=today)
        nudges = Nudge.objects.filter(target=assignment.worker,
                                      timestamp__range=today_range).order_by('-timestamp')
        epoch = (datetime.min if len(nudges) == 0
                              else nudges[0].timestamp)
        since = datetime.now() - epoch

        if since >= NUDGE_GRACE_PERIOD:
            email.nudge_notify(self)


class Bone(models.Model):
    target = models.ForeignKey(NamelessWorker,
                               related_name='bones', null=False)
    timestamp = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return "%s nudged @ %s" % (unicode(self.target), unicode(self.timestamp))

    def save(self, *args, **kwargs):
        super(Bone, self).save(*args, **kwargs)
        email.bone_notify(self)

