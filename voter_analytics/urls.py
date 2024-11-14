from django.urls import path
from .views import VoterListView, VoterGraphsView, VoterDetailView

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    path('graphs/', VoterGraphsView.as_view(), name='graphs'),
]
