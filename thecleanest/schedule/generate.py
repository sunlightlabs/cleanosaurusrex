"""Logic for generating assignments. The basic logic is:
       Find the latest assignment.
       Select the next worker in the cycle.
       If that worker has a credit pending, schedule the worker associated with the corresponding debit and mark the credit as used.
       Otherwise if the worker as a coupon pending, schedule the next worker in the cycle, and mark the coupon as used.
       Rinse and repeat.
"""
from django.conf import settings
from datetime import date, timedelta
from thecleanest.notifications import email
from thecleanest.schedule.models import NamelessWorker, Assignment, Debit, Credit, Coupon
from thecleanest.schedule.workeriter import AlphaWorkerIter
from thecleanest.schedule.workdays import workdays
from itertools import islice, izip, takewhile

def bootstrap_schedule():
    start_date = date.today()
    stop_date = date.today() + timedelta(days=settings.SCHED_HORIZON)
    days_to_schedule = list(takewhile(lambda d: d < stop_date,
                                      workdays(start_date)))

    future = izip(days_to_schedule,
                  AlphaWorkerIter())
    for (day, worker) in islice(future, 0, settings.SCHED_HORIZON):
        print "Bootstrapping %s" % (str(day), )
        a = Assignment(worker=worker, date=day)
        a.save()
        email.assignment_notify(a)

def generate_schedule():
    assignments = Assignment.objects.filter().order_by('-date')[:1]
    if len(assignments) == 0:
        return bootstrap_schedule()

    latest_assignment = assignments[0]
    credits_for_date = Credit.objects.filter(skipped_date=latest_assignment.date)
    if len(credits_for_date) == 0:
        coupons_for_date = Coupon.objects.filter(skipped_date=latest_assignment.date)
        if len(coupons_for_date) == 0:
            start_worker = latest_assignment.worker
        else:
            start_worker = coupons_for_date[0].worker
    else:
        start_worker = credits_for_date[0].worker

    try:
        workers = AlphaWorkerIter(after=start_worker)
    except Exception as e:
        print "Unable to generate assignments:"
        print str(e)
        return

    start_date = latest_assignment.date + timedelta(days=1)
    stop_date = date.today() + timedelta(days=settings.SCHED_HORIZON)
    print "Schedule horizon: %s" % str(stop_date)
    if start_date >= stop_date:
        print "No need to schedule anything."
        return

    print "Latest assignment: %s" % str(latest_assignment.date)
    days_to_schedule = list(takewhile(lambda d: d < stop_date,
                                      workdays(latest_assignment.date + timedelta(days=1))))

    print "Scheduling %d days: %r" % (len(days_to_schedule), days_to_schedule)

    for day in days_to_schedule:
        print "Assigning %s" % (str(day), )

        worker = workers.next()
        credits = worker.unused_credits().order_by('timestamp')
        if len(credits) > 0:
            earliest_credit = credits[0]
            earliest_credit.skipped_date = day
            earliest_credit.save()
            new_assignment = Assignment(worker=earliest_credit.debit.worker,
                                        date=day)
            new_assignment.save()

            email.assignment_notify(new_assignment)

        else:
            coupons = worker.unused_coupons().order_by('timestamp')
            while len(coupons) > 0:
                earliest_coupon = coupons[0]
                earliest_coupon.skipped_date = day
                earliest_coupon.save()
                worker = workers.next()
                coupons = worker.unused_coupons().order_by('timestamp')

            new_assignment = Assignment(worker=worker,
                                        date=day)
            new_assignment.save()

            email.assignment_notify(new_assignment)





if __name__ == "__main__":
    print generate_schedule()

