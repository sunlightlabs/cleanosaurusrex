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

from datetime import date, timedelta
from thecleanest.schedule.models import NamelessWorker, Assignment, Debit, Credit, Coupon
from thecleanest.schedule.workeriter import AlphaWorkerIter
from thecleanest.schedule.workdays import workdays
from itertools import islice, izip, dropwhile, takewhile
from settings import SCHED_HORIZON

def bootstrap_schedule():
    start_date = date.today()
    stop_date = date.today() + timedelta(days=SCHED_HORIZON)
    days_to_schedule = list(takewhile(lambda d: d < stop_date,
                                      workdays(start_date)))

    future = izip(days_to_schedule,
                  AlphaWorkerIter())
    for (day, worker) in islice(future, 0, SCHED_HORIZON):
        print "Bootstrapping %s" % (str(day), )
        a = Assignment(worker=worker, date=day)
        a.save()
    
def generate_schedule():
    assignments = Assignment.objects.filter().order_by('-date')[:1]
    if len(assignments) == 0:
        return bootstrap_schedule()

    latest_assignment = assignments[0]

    workers = AlphaWorkerIter(start=latest_assignment.worker)

    start_date = latest_assignment.date + timedelta(days=1)
    stop_date = date.today() + timedelta(days=SCHED_HORIZON)
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
        credits = Credit.objects.filter(worker=worker, 
                                        skipped_date__isnull=True).order_by('timestamp')
        if len(credits) > 0:
            earliest_credit = credits[0]
            earliest_credit.skipped_date = day
            earliest_credit.save()
            new_assignment = Assignment(worker=earliest_credit.debit.worker,
                                        date=day)
            new_assignment.save()
        else:
            coupons = Coupon.objects.filter(worker=worker,
                                            skipped_date__isnull=True).order_by('timestamp')
            if len(coupons) > 0:
                earliest_coupon = coupons[0]
                earliest_credit.skipped_date = day
                earliest_coupon.save()
                worker = workers.next()

            new_assignment = Assignment(worker=worker,
                                        date=day)
            new_assignment.save()





if __name__ == "__main__":
    print generate_schedule()
    
