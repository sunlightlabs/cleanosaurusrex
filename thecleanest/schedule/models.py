from django.db import models
from django.db.models import Q
from thecleanest.notifications import email
import random
import datetime
import uuid

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

def generate_uuid():
    return uuid.uuid4().hex

class NamelessWorker(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    avatar_url = models.URLField(verify_exists=False, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def balance(self):
        return self.credits.count() - self.debits.count()

    def unused_credits(self):
        return self.credits.filter(skipped_date__isnull=True)

    def unused_coupons(self):
        return self.coupons.filter(skipped_date__isnull=True)


class AssignmentManager(models.Manager):

    def current_assignment(self):
        try:
            return Assignment.objects.get(date=datetime.date.today())
        except Assignment.DoesNotExist:
            pass # just return None

class Assignment(models.Model):
    date = models.DateField(null=False, blank=False, unique=True)
    worker = models.ForeignKey(NamelessWorker, related_name='assignments', null=False)
    defer_code = models.CharField(max_length=32, default=generate_uuid)

    objects = AssignmentManager()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return "%s %s" % (self.date, self.worker.full_name())

    def is_complete(self):
        return self.date < datetime.date.today()

    def eligible_defer_targets(self):
        # get a range of a week before and after this assignment
        week_before = self.date - datetime.timedelta(7)
        week_after = self.date + datetime.timedelta(7)

        # get a list of worker ids that have deferred within this 2 week range
        deferred_worker_ids = NamelessWorker.objects.filter(
            debits__skipped_assignment__date__range=(week_before, week_after)
        ).values_list('pk', flat=True)

        eligible_workers = NamelessWorker.objects.exclude(
            Q(pk=self.worker.pk) | Q(pk__in=deferred_worker_ids) | Q(is_active=False)
        )
        return eligible_workers

    def defer(self):

        today = datetime.date.today()

        if today > self.date:
            raise ValueError('unable to defer assignments that have already been completed')

        eligible_workers = self.eligible_defer_targets()
        # get a random worker that isn't the current one or a recently deferring worker
        # or an inactive worker.
        eligible_workers.sort(key=random.random)
        new_worker = eligible_workers[0]

        # create the debit
        debit = Debit.objects.create(
            worker=self.worker,
            skipped_assignment=self,
        )

        # create the credit
        credit = Credit.objects.create(
            debit=debit,
            worker=new_worker,
        )

        # resassign worker on current assignment
        self.worker = new_worker
        self.defer_code = generate_uuid()
        self.save()

        email.defer_notify(debit)

        return debit

    def defer_to(self, new_worker):
        assert isinstance(new_worker, NamelessWorker)
        debit = Debit.objects.create(
            worker=self.worker,
            skipped_assignment=self
        )

        credit = Credit.objects.create(
            debit=debit,
            worker=new_worker
        )

        self.worker = new_worker
        self.defer_code = generate_uuid()
        self.save()

        email.defer_notify(debit)

        return debit


class Debit(models.Model):
    worker = models.ForeignKey(NamelessWorker, related_name='debits', null=False)
    skipped_assignment = models.ForeignKey(Assignment, related_name='debits', null=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        ordering = ('timestamp',)

    def __unicode__(self):
        return "%s skipped %s" % (self.worker.full_name(), self.skipped_assignment.date)

class Credit(models.Model):
    debit = models.ForeignKey(Debit, related_name='credits', null=True)
    worker = models.ForeignKey(NamelessWorker, related_name='credits', null=False)
    # skipped_date is set when the generation function uses the credit
    skipped_date = models.DateField(default=None, null=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

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

