from django.db import models

class NamelessWorker(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    is_active = models.BooleanField(default=False)

class Assignment(models.Model):
    date = models.DateField(null=False, blank=False)
    debit = models.ForeignKey('Debit', null=True)  # points to original deferral object
    worker = models.ForeignKey(NamelessWorker, null=False)

class Debit(models.Model):
    skipped_assignment = models.ForeignKey(Assignment, related_name='skipped_by', 
                                           null=False)
    new_assignment = models.ForeignKey(Assignment, related_name='created_for',
                                       null=True)
    parent_debit = models.ForeignKey('Debit', null=True)
    original_worker = models.ForeignKey(NamelessWorker, null=False)
    timestamp = models.DateTimeField(null=False)

class Credit(models.Model):
    spawning_debit = models.ForeignKey(Debit, related_name='spawned_credit', 
                                       null=True)
    credited_debit = models.ForeignKey(Debit, related_name='satisfying_credit', 
                                       null=True)
    worker = models.ForeignKey(NamelessWorker, null=False)
    timestamp = models.DateTimeField(null=False)
    note = models.CharField(max_length=5000, null=True)
    is_used = models.BooleanField(default=False)




"""

deferrment_iter():

    for d in deferrment where timestamp > 2 weeks from now:

        yield d

worker_iter():

    for d in deferrment_iter:

        yield d

    for w in worker:

        yield w

for day in next_n_weeks:

    if day.is_work_day:

        worker = worker_iter.next

        new assignment(day, worker)




"""
