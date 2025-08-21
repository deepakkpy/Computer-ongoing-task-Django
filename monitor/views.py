
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from .models import Computer, Snapshot, Process
from .serializers import ComputerSerializer, SnapshotSerializer
from .permissions import HasAgentApiKey

class IngestView(APIView):
    permission_classes = [HasAgentApiKey]

    @transaction.atomic
    def post(self, request):
        data = request.data
        hostname = data.get('hostname')
        if not hostname:
            return Response({'detail': 'hostname required'}, status=400)

        sysinfo = data.get('system', {}) or {}
        processes = data.get('processes', [])

        computer, _ = Computer.objects.get_or_create(hostname=hostname)
        computer.last_seen = timezone.now()
        computer.save()

        snap = Snapshot.objects.create(
            computer=computer,
            os=sysinfo.get('os',''),
            cpu_model=sysinfo.get('cpu_model',''),
            cores=sysinfo.get('cores',0),
            threads=sysinfo.get('threads',0),
            ram_total_gb=sysinfo.get('ram_total_gb',0),
            ram_used_gb=sysinfo.get('ram_used_gb',0),
            ram_available_gb=sysinfo.get('ram_available_gb',0),
            storage_total_gb=sysinfo.get('storage_total_gb',0),
            storage_used_gb=sysinfo.get('storage_used_gb',0),
            storage_free_gb=sysinfo.get('storage_free_gb',0),
        )

        objs = [
            Process(snapshot=snap,
                    pid=p.get('pid',0),
                    ppid=p.get('ppid',0),
                    name=p.get('name',''),
                    cpu=p.get('cpu',0.0),
                    mem_mb=p.get('mem_mb',0.0))
            for p in processes
        ]
        Process.objects.bulk_create(objs, batch_size=1000)

        return Response({'snapshot_id': snap.id, 'created_at': snap.created_at})

class ComputersView(APIView):
    def get(self, request):
        qs = Computer.objects.all().order_by('hostname')
        return Response(ComputerSerializer(qs, many=True).data)

class LatestSnapshotView(APIView):
    def get(self, request, hostname):
        computer = get_object_or_404(Computer, hostname=hostname)
        snap = computer.snapshots.first()
        if not snap:
            return Response({'detail': 'no data'}, status=404)
        return Response(SnapshotSerializer(snap).data)

class SnapshotListView(APIView):
    def get(self, request, hostname):
        computer = get_object_or_404(Computer, hostname=hostname)
        qs = computer.snapshots.all().only('id','created_at')
        return Response([{'id': s.id, 'created_at': s.created_at} for s in qs])

class SnapshotDetailView(APIView):
    def get(self, request, pk):
        snap = get_object_or_404(Snapshot, pk=pk)
        return Response(SnapshotSerializer(snap).data)
