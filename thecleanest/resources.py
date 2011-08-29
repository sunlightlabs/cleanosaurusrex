from tastypie import fields
from tastypie.resources import ModelResource
from thecleanest.schedule.models import NamelessWorker, Assignment, Debit, Credit

class NamelessWorkerResource(ModelResource):
    assignments = fields.ToManyField('thecleanest.resources.AssignmentResource', 'assignments')

    class Meta:
        queryset = NamelessWorker.objects.all()
        resource_name = 'namelessworker'

class AssignmentResource(ModelResource):
    class Meta:
        queryset = Assignment.objects.all()
        resource_name = 'assignment'

class DebitResource(ModelResource):
    class Meta:
        queryset = Debit.objects.all()

class CreditResource(ModelResource):
    class Meta:
        queryset = Credit.objects.all()