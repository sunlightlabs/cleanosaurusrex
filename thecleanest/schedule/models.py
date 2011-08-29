from django.db import models

class NamelessWorker(models.Model):

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    is_active = models.BooleanField(default=False)


class Assignment(models.Model):
    date
    debit ? # points to original deferral object
    worker

class Debit(models.Model):
    skipped_assignment
    new_assignment ?
    parent_debit ?
    original_worker
    timestamp

class Credit(models.Model):
    spawning_debit ?
    credited_debit ?
    worker
    timestamp
    note
    is_used = false




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