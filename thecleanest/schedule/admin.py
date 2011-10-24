from django.contrib import admin
from thecleanest.schedule.models import NamelessWorker, Assignment, Credit, Debit

class NamelessWorkerAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_editable = ('is_active',)
admin.site.register(NamelessWorker, NamelessWorkerAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'worker', 'is_complete')
    readonly_fields = ('defer_code',)
admin.site.register(Assignment, AssignmentAdmin)

admin.site.register(Credit)
admin.site.register(Debit)