from django.db import models

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

class Assignment(models.Model):
    date = models.DateField(null=False, blank=False, unique=True)
    worker = models.ForeignKey(NamelessWorker, null=False)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return "%s %s" % (self.date, self.worker.full_name())

class Debit(models.Model):
    worker = models.ForeignKey(NamelessWorker, related_name='debits', null=False)
    skipped_date = models.DateField(null=False)
    timestamp = models.DateTimeField(null=False)

    class Meta:
        ordering = ('timestamp',)

    def __unicode__(self):
        return "%s skipped %s" % (self.worker.full_name(), self.skipped_date)

class Credit(models.Model):
    # debit is null if the credit was created by decree
    debit = models.ForeignKey(Debit, null=True)
    worker = models.ForeignKey(NamelessWorker, related_name='credits', null=False)
    # skipped_date is set when the generation function uses the credit
    skipped_date = models.DateField(default=None, null=True)
    note = models.CharField(max_length=5000, null=True)
    timestamp = models.DateTimeField(null=False)

    class Meta:
        ordering = ('timestamp',)

    def __unicode__(self):
        return "%s credited to %s" % (self.debit, self.worker.full_name())

