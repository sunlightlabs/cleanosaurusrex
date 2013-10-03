# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from thecleanest.notifications import email
import math
import random
import datetime
import uuid
from itertools import chain

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

def weighted_choice(pairs):
    """
    Takes a list of 2-tuples of the form (value, weight)
    and randomly chooses a value, in weighted fashion.
    """
    # Calculate a mean weight
    weights = [weight for (value, weight) in pairs if weight is not None]
    mean_weight = float(sum(weights)) / len(weights) if len(weights) > 0 else float('NaN')

    # Replace missing weights with the mean weight
    pairs = [(value, weight or mean_weight)
             for (value, weight) in pairs]

    total_weight = sum((weight for (value, weight) in pairs))
    rnd = random.random() * total_weight
    for (idx, (value, weight)) in enumerate(pairs):
        rnd -= weight
        if rnd < 0:
            return value

class NamelessWorkerManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(NamelessWorkerManager, self).__init__(*args, **kwargs)
        self.min_assignment_interval = None

    def cycle_length_in_days(self):
        return int(math.floor(self.filter(is_active=True).count() * float(7) / float(5)))


class NamelessWorker(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    avatar_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=False)
    deferral_exempt = models.BooleanField(default=False)
    objects = NamelessWorkerManager()

    class Meta:
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def balance(self):
        return self.credits.count() - self.debits.count()

    def unused_credits(self):
        return self.credits.filter(skipped_date__isnull=True)

    def unused_coupons(self):
        return self.coupons.filter(skipped_date__isnull=True)

    def assignment_interval(self):
        credit_dates = [c.timestamp.date() for c in self.credits.all()]
        debit_dates = [d.timestamp.date() for d in self.debits.all()]
        assign_dates = [a.date for a in self.assignments.all()]
        all_dates = list(chain(credit_dates, debit_dates, assign_dates, [datetime.date.today()]))
        if len(all_dates) >= 2:
            earliest_date = min(all_dates)
            latest_date = max(all_dates)
            timespan = latest_date - earliest_date
            assign_count = self.assignments.count()
            return timespan.days / assign_count
        else:
            return None

    def deferral_weight(self):
        ival = self.assignment_interval()
        if ival is None:
            return None
        return float(ival) / NamelessWorker.objects.cycle_length_in_days()

    def latest_assignment(self):
        today = datetime.date.today()
        assignments = list(self.assignments.filter(date__lt=today).order_by('-date'))
        if assignments:
            return assignments[0]
        else:
            return None

    def pending_assignments(self):
        return self.assignments.filter(date__gte=datetime.date.today())

    def unsatisfied_debits(self):
        return Debit.objects.filter(credits__skipped_date=None, worker=self)

    def defer_pending_assignments(self):
        for ass in self.pending_assignments():
            ass.defer()

    def satisfy_debits(self):
        for debit in self.unsatisfied_debits():
            for credit in debit.credits.all():
                note = u"From deactivation of {name}".format(name=self.full_name())
                credit.convert_to_coupon(note)

    def deactivate(self):
        self.is_active = False
        self.save()

        self.defer_pending_assignments()
        self.satisfy_debits()


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
        return u"%s %s" % (self.date, self.worker.full_name())

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

        # We want to exclude the people who have a pending assignment
        assigned_worker_ids = NamelessWorker.objects.filter(
            assignments__date__gt=datetime.date.today()
        ).values_list('pk', flat=True)

        eligible_workers = NamelessWorker.objects.exclude(
            Q(pk=self.worker.pk)
            | Q(pk__in=deferred_worker_ids)
            | Q(pk__in=assigned_worker_ids)
            | Q(is_active=False)
            | Q(deferral_exempt=True)
        )

        # Workers who have had kitchen duty multiple times per cycle
        # should be ignored. We use only 80% of the cycle length to
        # avoid depleting the pool too much during common vacation periods.
        ival_threshold = int(math.floor(NamelessWorker.objects.cycle_length_in_days() * float(0.8)))
        eligible_workers = [w
                            for w in eligible_workers
                            if w.assignments.count() >= 2
                            and w.assignment_interval() >= ival_threshold]

        return eligible_workers

    def defer(self):

        today = datetime.date.today()

        if today > self.date:
            raise ValueError('unable to defer assignments that have already been completed')

        eligible_workers = self.eligible_defer_targets()
        weighted_workers = [(w, w.deferral_weight())
                            for w in eligible_workers]
        new_worker = weighted_choice(weighted_workers)

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
        return u"%s skipped %s" % (self.worker.full_name(), self.skipped_assignment.date)

class Credit(models.Model):
    debit = models.ForeignKey(Debit, related_name='credits', null=True)
    worker = models.ForeignKey(NamelessWorker, related_name='credits', null=False)
    # skipped_date is set when the generation function uses the credit
    # A skipped_date of 1970-01-01 means canceled.
    skipped_date = models.DateField(default=None, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __unicode__(self):
        return u"%s credited to %s" % (self.debit, self.worker.full_name())

    def convert_to_coupon(self, note=None):
        self.skipped_date = datetime.date(1970, 1, 1)
        self.save()

        coupon = Coupon.objects.create(
            worker=self.worker,
            note=(note or u'Converted from Credit(pk={})'.format(self.pk)),
            credit=self)
        return coupon

class Coupon(models.Model):
    worker = models.ForeignKey(NamelessWorker, related_name='coupons', null=False)
    skipped_date = models.DateField(default=None, null=True)
    note = models.CharField(max_length=5000, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    credit = models.OneToOneField(Credit, null=True)

class Rating(models.Model):
    assignment = models.ForeignKey(Assignment, related_name="ratings")
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    value = models.IntegerField(choices=RATINGS)
    subject_of_judgement = models.CharField(max_length=1, choices=SUBJECTS)

    class Meta:
        ordering = ('-timestamp',)

    def __unicode__(self):
        pass

