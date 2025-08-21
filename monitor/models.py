
from django.db import models

class Computer(models.Model):
    hostname = models.CharField(max_length=100, unique=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname

class Snapshot(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, related_name='snapshots')
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional system info
    os = models.CharField(max_length=200, blank=True, default='')
    cpu_model = models.CharField(max_length=200, blank=True, default='')
    cores = models.IntegerField(default=0)
    threads = models.IntegerField(default=0)
    ram_total_gb = models.FloatField(default=0)
    ram_used_gb = models.FloatField(default=0)
    ram_available_gb = models.FloatField(default=0)
    storage_total_gb = models.FloatField(default=0)
    storage_used_gb = models.FloatField(default=0)
    storage_free_gb = models.FloatField(default=0)

    class Meta:
        ordering = ['-created_at']

class Process(models.Model):
    snapshot = models.ForeignKey(Snapshot, on_delete=models.CASCADE, related_name='processes')
    pid = models.IntegerField()
    ppid = models.IntegerField()
    name = models.CharField(max_length=255)
    cpu = models.FloatField()
    mem_mb = models.FloatField()

    class Meta:
        indexes = [models.Index(fields=['pid', 'ppid'])]
        ordering = ['name', 'pid']
