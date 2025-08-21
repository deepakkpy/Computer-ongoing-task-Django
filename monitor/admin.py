
from django.contrib import admin
from .models import Computer, Snapshot, Process

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ('hostname','last_seen')

@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ('computer','created_at','cores','threads')

@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('snapshot','name','pid','ppid','cpu','mem_mb')
    list_filter = ('snapshot',)
