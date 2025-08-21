
from django.urls import path
from .views import IngestView, ComputersView, LatestSnapshotView, SnapshotListView, SnapshotDetailView

urlpatterns = [
    path('ingest/', IngestView.as_view()),
    path('computers/', ComputersView.as_view()),
    path('computers/<str:hostname>/latest/', LatestSnapshotView.as_view()),
    path('snapshots/<str:hostname>/', SnapshotListView.as_view()),
    path('snapshots/id/<int:pk>/', SnapshotDetailView.as_view()),
]
