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
