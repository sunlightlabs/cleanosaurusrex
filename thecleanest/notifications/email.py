import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def assignment_notify(assignment):

    if assignment.worker.email is None:
        return

    data = {
        'now': datetime.datetime.now(),
        'assignment': assignment,
        'enddate': assignment.date + datetime.timedelta(1),
        'worker': assignment.worker,
    }

    msg = EmailMessage(
        subject="[Cleanosaurus Rex] Rawr! You've got kitchen duty!!!",
        body=render_to_string('email/assignment.txt', data),
        from_email=settings.EMAIL_SENDER,
        to=(settings.EMAIL_RECIPIENT or assignment.worker.email,),
    )

    cal = render_to_string('email/assignment.ics', data)

    msg.attach('rexassignment%s.ics' % assignment.pk, cal, 'text/calendar')
    msg.send()

def assignment_today(assignment):

    if assignment.worker.email is None:
        return

    data = {
        'assignment': assignment,
        'worker': assignment.worker,
    }

    msg = EmailMessage(
        subject="[Cleanosaurus Rex] Rawr-minder! You've got kitchen duty TODAY!!!",
        body=render_to_string('email/assignment_today.txt', data),
        from_email=settings.EMAIL_SENDER,
        to=(settings.EMAIL_RECIPIENT or assignment.worker.email,),
    )
    msg.send()

def assignment_next_week(assignment):

    if assignment.worker.email is None:
        return

    data = {
        'assignment': assignment,
        'worker': assignment.worker,
    }

    msg = EmailMessage(
        subject="[Cleanosaurus Rex] Rawr-minder! You've got kitchen duty next week!!!",
        body=render_to_string('email/assignment_week.txt', data),
        from_email=settings.EMAIL_SENDER,
        to=(settings.EMAIL_RECIPIENT or assignment.worker.email,),
    )
    msg.send()

def defer_notify(debit):

    if debit.worker.email is None:
        return

    data = {
        'worker': debit.skipped_assignment.worker,
        'slacker': debit.worker,
        'date': debit.skipped_assignment.date,
        'assignment': debit.skipped_assignment,
    }

    # message to worker deferring their day

    msg = EmailMessage(
        subject="[Cleanosaurus Rex] Cleanosaurus: Working around your conflicts since 2011",
        body=render_to_string('email/defer_slacker.txt', data),
        from_email=settings.EMAIL_SENDER,
        to=(settings.EMAIL_RECIPIENT or debit.worker.email,),
    )
    msg.send()

    # message to the person that was swapped in

    msg = EmailMessage(
        subject="[Cleanosaurus Rex] Rawr! You've got kitchen duty!!!",
        body=render_to_string('email/defer_worker.txt', data),
        from_email=settings.EMAIL_SENDER,
        to=(settings.EMAIL_RECIPIENT or debit.skipped_assignment.worker.email,),
    )
    msg.send()

def nudge_notify(nudge):

    if nudge.target.email is None:
        return

    data = {'slacker': nudge.target}

    msg = EmailMessage(
        subject='[Cleanosaurus Rex] Rawr! Sooooo angry at you...',
        body=render_to_string('email/nudge.txt', data),
        from_email=settings.EMAIL_SENDER,
        to=(settings.EMAIL_RECIPIENT or nudge.target.email,),
    )
    msg.send()


def bone_notify(bone):

    if bone.target.email is None:
        return

    data = {'worker': bone.target}

    msg = EmailMessage(
        subject='[Cleanosaurus Rex] Grrrrreat job!',
        body=render_to_string('email/bone.txt', data),
        from_email=settings.EMAIL_SENDER,
        to=(settings.EMAIL_RECIPIENT or bone.target.email,),
    )
    msg.send()
