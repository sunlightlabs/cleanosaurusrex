from schedule.models import NamelessWorker, Assignment

class AlphaWorkerIter(object):
    """Iterates through active workers, in alphabetical order, starting at
    given `start` worker. The iterator never stops. Instead it wraps infinitely."""
    def __init__(self, start=None):
        assert isinstance(start, (NamelessWorker, type(None)))
        self._workers = [w for w in NamelessWorker.objects.filter(is_active=True,
                                                                 ).order_by('last_name', 
                                                                            'first_name')]
        if start is not None:
            while self._workers[0] != start:
                self._workers.append(self._workers.pop())
 
    def __iter__(self):
        return self

    def next(self):
        try:
            w = self._workers.pop()
        except IndexError:
            raise StopIteration()
        self._workers.append(w)
        return NamelessWorker(id=w.id)

class WorkerAssignmentIter(object):
    """Represents the normal assignment cycle, which is alphabetical.
       New instances use the latest-scheduled assignment that is not
       the result of a debit."""

    def __init__(self):
        last_natural_assign = Assignment.objects.filter(debit__isnull=True
                                                       ).order_by(date='DESC')[0]
        if last_natural_assign is None:
            self._worker_iter = AlphaWorkerIter()
        else:
            self._worker_iter = AlphaWorkerIter(start=last_natural_assign.worker)

    def __iter__(self):
        return self

    def next(self):
        return self._worker_iter.next()

