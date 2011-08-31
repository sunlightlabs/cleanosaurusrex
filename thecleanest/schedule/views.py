
from datetime import datetime, date, timedelta
from django.db.models import Count
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.core.serializers import serialize, deserialize
from schedule.models import Assignment, Debit, Credit, NamelessWorker
from notifications.models import Bone, Nudge
import calendar

def index(request):

    current_assignment = Assignment.objects.current_assignment()

    context = {
        'current_assignment': current_assignment,
    }

    return render(request, "index.html", context)

def hall_of_fame(request):

    most_boned = NamelessWorker.objects.annotate(num_bones=Count('bones')).filter(num_bones__gt=0).order_by('-num_bones')[:10]

    context = {
        'most_boned': most_boned,
    }

    return render(request, 'hall_of_fame.html', context)

def hall_of_shame(request):

    most_deferred = NamelessWorker.objects.annotate(num_debits=Count('debits')).filter(num_debits__gt=0).order_by('-num_debits')[:10]
    most_nudged = NamelessWorker.objects.annotate(num_nudges=Count('nudges')).filter(num_nudges__gt=0).order_by('-num_nudges')[:10]

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
    assignment = Assignment.objects.current_assignment()
    today = date.today()
    today_weekday = calendar.weekday(today.year, today.month, today.day)
    today_range = (datetime(today.year, today.month, today.day, 0, 0, 0),
                   datetime(today.year, today.month, today.day, 23, 59, 59))
    monday = date.today() - timedelta(days=today_weekday)
    assignments = Assignment.objects.filter(date__gte=monday).order_by('date')[:10]
    week1_assignments = assignments[0:5]
    week2_assignments = assignments[5:10]
    bone_count = Bone.objects.filter(timestamp__range=today_range).count()
    nudge_count = Nudge.objects.filter(timestamp__range=today_range).count()

    return render_to_response('schedule.html', {
                                  'today': str(today),
                                  'monday': str(monday),
                                  'assignments': assignments,
                                  'week1_assignments': week1_assignments,
                                  'week2_assignments': week2_assignments,
                                  'current_assignment': assignment,
                                  'bone_count': bone_count,
                                  'nudge_count': nudge_count
                              })

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

