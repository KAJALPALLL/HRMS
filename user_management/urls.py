from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register,name='register'),
    path('client-register',views.client_register,name='client_register'),
    path('',views.login,name='login'),
    path('add-employee',views.add_employee,name='add_employee'),
    path('employee-list',views.employee_list,name='employee_list'),
    path('update-employee/<str:id>',views.update_employee,name='update_employee'),
    path('delete-employee/<str:id>',views.delete_employee,name='delete_employee'),
    path('my-leave-list',views.my_leave_list,name='my_leave_list'),
    path('my-profile',views.my_profile,name='my_profile'),
    path('employee-leave-list/<str:id>',views.employee_leave_list,name='employee_leave_list'),
    path('add-documents',views.add_documents,name='add_documents'),
    path('employee-document-list/<str:id>',views.employee_document_list,name='employee_document_list'),
    path('documents-list',views.documents_list,name='documents_list'),
    path('export-leave',views.export_leave,name='export_leave'),
    path('export-client-report/<str:id>',views.export_client_report,name='export_client_report'),
    path('client-list',views.client_list,name='client_list'),
    path('select-department/<str:id>',views.select_department,name='select_department'),
    path('logout',views.logout,name='logout'),

]

