
from rest_framework import serializers
from .models import Computer, Snapshot, Process

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ['id','pid','ppid','name','cpu','mem_mb']

class SnapshotSerializer(serializers.ModelSerializer):
    processes = ProcessSerializer(many=True, read_only=True)
    class Meta:
        model = Snapshot
        fields = ['id','created_at','os','cpu_model','cores','threads','ram_total_gb','ram_used_gb','ram_available_gb','storage_total_gb','storage_used_gb','storage_free_gb','processes']

class ComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields = ['id','hostname','last_seen']
