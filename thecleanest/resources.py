from datetime import date
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.http import HttpBadRequest, HttpCreated
from tastypie.resources import ModelResource
from thecleanest.schedule.models import NamelessWorker, Assignment, Debit, Credit
from thecleanest.notifications.models import Nudge, Bone

class NamelessWorkerResource(ModelResource):
    assignments = fields.ToManyField('thecleanest.resources.AssignmentResource', 'assignments')

    class Meta:
        queryset = NamelessWorker.objects.all()
        resource_name = 'namelessworker'

class AssignmentResource(ModelResource):
    worker = fields.ToOneField(NamelessWorkerResource, 'worker')

    class Meta:
        allowed_methods = ['get','post']
        authorization= Authorization()
        queryset = Assignment.objects.all()
        resource_name = 'assignment'
        filtering = {
            "date": ('exact', 'lte', 'gte')
        }

    def post_detail(self, request, **kwargs):

        if 'defer' in request.POST:

            assignment = Assignment.objects.get(pk=kwargs['pk'])
            debit = assignment.defer()

            debit_res = DebitResource()
            location = debit_res.get_resource_uri(debit)

            return HttpCreated(location=location)

        return HttpBadRequest()

class DebitResource(ModelResource):
    credits = fields.ToManyField('thecleanest.resources.CreditResource', 'credits')
    worker = fields.ToOneField(NamelessWorkerResource, 'worker')
    skipped_assignment = fields.ToOneField(AssignmentResource, 'skipped_assignment')

    class Meta:
        queryset = Debit.objects.all()

class CreditResource(ModelResource):
    debit = fields.ToOneField(DebitResource, 'debit')
    worker = fields.ToOneField(NamelessWorkerResource, 'worker')

    class Meta:
        queryset = Credit.objects.all()


class NudgeResource(ModelResource):
    target = fields.ToOneField(NamelessWorkerResource, 'target')
    class Meta:
        allowed_methods = ['get','post']
        authorization= Authorization()
        resource_name = 'nudge'
        queryset = Nudge.objects.all()

    def post_detail(self, request, **kwargs):
        today = date.today()
        assignment = Assignment.objects.current_assignment()
        if assignment is not None:
            ndg = Nudge(target=assignment.worker)
            ndg.save()
            ndg_res = NudgeResource()
            ndg_location = ndg_res.get_resource_uri(ndg)
            return HttpCreated(location=ndg_location)
        else:
            return HttpBadRequest()

class BoneResource(ModelResource):
    target = fields.ToOneField(NamelessWorkerResource, 'target')
    class Meta:
        allowed_methods = ['get', 'post']
        authorization = Authorization()
        resource_name = 'bone'
        queryset = Bone.objects.all()

    def post_detail(self, request, **kwargs):
        assignment = Assignment.objects.current_assignment()
        if assignment is not None:
            bn = Bone(target=assignment.worker)
            bn_res = BoneResource()
            bn_location = bn_res.get_resource_uri(bn)
            return HttpCreated(location=bn_location)
        else:
            return HttpBadRequest()



