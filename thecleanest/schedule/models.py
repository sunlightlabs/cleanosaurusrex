from django.db import models
import datetime

RATINGS = (
    (-2, 'Absolutely disgusting; you should be ashamed of yourself.'),
    (-1, 'Kind of gross.'),
    (0, 'Meh.'),
    (1, 'Decent job.'),
    (1, 'I am proud to call you my colleague in cleanliness.'),
)

SUBJECTS = (
    ('O', 'Organization'),
    ('W', 'Worker'),
)

class NamelessWorker(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

class AssignmentManager(models.Manager):

    def current_assignment(self):
        try:
            return Assignment.objects.get(date=datetime.date.today())
        except Assignment.DoesNotExist:
            pass # just return None

class Assignment(models.Model):
    date = models.DateField(null=False, blank=False, unique=True)
    worker = models.ForeignKey(NamelessWorker, related_name='assignments', null=False)

    objects = AssignmentManager()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return "%s %s" % (self.date, self.worker.full_name())

    def is_complete(self):
        return self.date < datetime.date.today()

class Debit(models.Model):
    worker = models.ForeignKey(NamelessWorker, related_name='debits', null=False)
    skipped_assignment = models.ForeignKey(Assignment, related_name='debits', null=True)
    timestamp = models.DateTimeField(null=False)

    class Meta:
        ordering = ('timestamp',)

    def __unicode__(self):
        return "%s skipped %s" % (self.worker.full_name(), self.skipped_assignment.date)

class Credit(models.Model):
    debit = models.ForeignKey(Debit, related_name='credits', null=True)
    worker = models.ForeignKey(NamelessWorker, related_name='credits', null=False)
    # skipped_date is set when the generation function uses the credit
    skipped_date = models.DateField(default=None, null=True)
    timestamp = models.DateTimeField(null=False)
    class Meta:
        ordering = ('timestamp',)

    def __unicode__(self):
        return "%s credited to %s" % (self.debit, self.worker.full_name())

class Coupon(models.Model):
    worker = models.ForeignKey(NamelessWorker, related_name='coupons', null=False)
    skipped_date = models.DateField(default=None, null=True)
    note = models.CharField(max_length=5000, null=True)
    timestamp = models.DateTimeField(null=False)

class Rating(models.Model):
    assignment = models.ForeignKey(Assignment, related_name="ratings")
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    value = models.IntegerField(choices=RATINGS)
    subject_of_judgement = models.CharField(max_length=1, choices=SUBJECTS)

    class Meta:
        ordering = ('-timestamp',)

    def __unicode__(self):
        pass

