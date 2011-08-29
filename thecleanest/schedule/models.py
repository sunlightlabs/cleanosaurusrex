from django.db import models

class NamelessWorker(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    is_active = models.BooleanField(default=False)

class Assignment(models.Model):
    date = models.DateField(null=False, blank=False, unique=True)
    worker = models.ForeignKey(NamelessWorker, null=False)

class Debit(models.Model):
    worker = models.ForeignKey(NamelessWorker, related_name='debits', null=False)
    skipped_date = models.DateField(null=False)
    timestamp = models.DateTimeField(null=False)

class Credit(models.Model):
    debit = models.ForeignKey(Debit, null=True)
    worker = models.ForeignKey(NamelessWorker, related_name='credits', null=False)
    # skipped_date is set when the generation function uses the credit
    skipped_date = models.DateField(default=None, null=True)
    timestamp = models.DateTimeField(null=False)

class Coupon(models.Model):
    worker = models.ForeignKey(NamelessWorker, related_name='coupons', null=False)
    skipped_date = models.DateField(default=None, null=True)
    note = models.CharField(max_length=5000, null=True)
    timestamp = models.DateTimeField(null=False)

