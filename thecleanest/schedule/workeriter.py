from schedule.models import NamelessWorker, Assignment

class AlphaWorkerIter(object):
    """Iterates through active workers, in alphabetical order, starting at
    given `start` worker. The iterator never stops. Instead it wraps infinitely."""
    def __init__(self, after=None):
        assert isinstance(after, (NamelessWorker, type(None)))
        self._workers = [w for w in NamelessWorker.objects.filter(is_active=True,
                                                                 ).order_by('last_name', 
                                                                            'first_name')]
        self.cycle_head = self._workers[0]

        if after is not None:
            while self._workers[-1] != after:
                w = self._workers.pop(0)
                self._workers.append(w)
                if self._workers[0] == self.cycle_head:
                    raise Exception('NamelessWorker specified is not in the assignment rotation. Did they quit?')
 
    def __iter__(self):
        return self

    def next(self):
        try:
            w = self._workers.pop(0)
        except IndexError:
            raise StopIteration()
        self._workers.append(w)
        return w

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

