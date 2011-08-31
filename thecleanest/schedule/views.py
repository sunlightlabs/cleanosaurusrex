
from datetime import datetime, date
from django.db.models import Count
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.core.serializers import serialize, deserialize
from schedule.models import Assignment, Debit, Credit, NamelessWorker

def hall_of_fame(request):
    pass

def hall_of_shame(request):

    most_deferred = NamelessWorker.objects.annotate(num_debits=Count('debits')).filter(num_debits__gt=0).order_by('-num_debits')[:20]
    most_nudged = NamelessWorker.objects.annotate(num_nudges=Count('nudges')).filter(num_nudges__gt=0).order_by('-num_nudges')[:20]

    context = {
        'most_deferred': most_deferred,
        'most_nudged': most_nudged,
    }

    return render(request, 'hall_of_shame.html', context)

def assignment_detail(request, assignment_id):

    assignment = get_object_or_404(Assignment, pk=assignment_id)

    context = {
        'assignment': assignment,
        'debits': Debit.objects.filter(skipped_assignment=assignment).select_related(),
    }

    return render(request, 'assignment_detail.html', context)

def defer_assignment(request, defer_code):

    try:

        assignment = Assignment.objects.get(defer_code=defer_code)

        if request.method == 'POST':
            assignment.defer()
            return HttpResponseRedirect('/')

    except Assignment.DoesNotExist:
        assignment = None

    return render(request, 'defer.html', {'assignment': assignment})

def worker_detail(request, worker_id):

    worker = get_object_or_404(NamelessWorker, pk=worker_id)

    context = {
        'worker': worker,
        'debits': Debit.objects.filter(worker=worker).select_related(),
    }

    return render(request, 'worker_detail.html', context)


def current_schedule(request):
    """JSON representation of the current schedule."""
    # Get current and future assignments
    return render_to_response('schedule.html')

def kitchen(request):
    assignment = Assignment.objects.current_assignment()
    if assignments is None:
        return Http404('No one is scheduled for kitchen duty!')
    else:
        return render_to_response('kitchen.html', {
                                      'worker': assignment.worker
                                  })

def assignments(request):
    assignments = Assignment.objects.all()
    assign_json = serialize('json', assignments)
    return HttpResponse(assign_json, mimetype='application/json')

def debits(request):
    debits = Debit.objects.all()
    debit_json = serialize('json', debits)
    return HttpResponse(debit_json, mimetype='application/json')

def credits(request):
    credits = Credit.objects.all()
    credit_json = serialize('json', credits)
    return HttpResponse(credit_json, mimetype='application/json')

