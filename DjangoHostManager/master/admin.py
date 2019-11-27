from django.contrib import admin
from .models import *
# Register your models here.

class ExecuteLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'hostip', 'hostuser', 'hostpass', 'hostcmd', 'excuteuser', 'excuteip', 'filepath', 'executetime')

admin.site.register(Business)
admin.site.register(HostGroup)
admin.site.register(Host)
admin.site.register(HostToHostGroup)
admin.site.register(ExecuteLog, ExecuteLogAdmin)