from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("references/", views.references, name="references"),
    path("references/<slug:slug>/", views.reference_detail, name="reference_detail"),
    path("contacts/", views.contacts, name="contacts"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("files/<int:pk>/download/", views.download_file, name="download_file"),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
