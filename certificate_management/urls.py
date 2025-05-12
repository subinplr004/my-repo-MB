from django.urls import path
from . import views

urlpatterns = [
    path('issue/', views.issue_certificate, name='issue-certificate'),
    path('verify/', views.verify_certificate_form, name='verify-certificate-form'),
    path('verify-certificate/<str:cert_id>/', views.verify_certificate, name='verify-certificate'),
    path('request-duplicate/', views.request_duplicate_certificate, name='request-duplicate'),
    path('request-duplicate/', views.request_duplicate_certificate, name='request-duplicate'),
    path('admin/duplicate-requests/', views.duplicate_requests_admin, name='admin-duplicate-requests'),
    path('admin/duplicate-requests/<int:request_id>/<str:new_status>/', views.update_duplicate_request_status, name='update-duplicate-status'),



]
