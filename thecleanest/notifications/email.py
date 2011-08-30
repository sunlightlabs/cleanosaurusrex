from django.core.mail import EmailMessage


def nudge_notify(nudge):
    if nudge.target.email is None:
        return

    msg = EmailMessage(subject='Nudge',
                       body='Cleanosaurus Rex is sad. Please clean the kitchen.',
                       from_email='Cleanosaurus Rex <cleanosaurus-rex@sunlightfoundation.com>',
                       to=nudge.target.email)
    msg.send()


def bone_notify(bone):
    if bone.target.email is None:
        return

    msg = EmailMessage(subject='Grrrrreat job!',
                       body='Your clean kitchen makes Cleanosaurus Rex purrrrrr.',
                       from_email='Cleanosaurus Rex <cleanosaurus-rex@sunlightfoundation.com',
                       to=bone.target.email)
    msg.send()
