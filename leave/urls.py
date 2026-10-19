from django.urls import path
from . import views

urlpatterns = [
    path('add-leave',views.add_leave_type,name='add_leave_type'),
    path('leave-list',views.leave_list,name='leave_list'),
    path('update-leave/<str:id>',views.update_leave_type,name='update_leave_type'),
    path('delete-leave/<str:id>',views.delete_leave_type,name='delete_leave_type'),

    # admin leave request list  and per employee list
    path('leave-request-list',views.leave_request_list,name='leave_request_list'),
    path('my-leave-request',views.my_leave_request,name='my_leave_request'),
    path('employee-leave-request/<str:id>',views.employee_leave_request,name='employee_leave_request'),

    # approved by admin
    path('leave-request-status/<str:id>',views.update_leave_request_status,name='update_leave_request_status'),
    path('update-employee-leave/<str:id>',views.update_employee_leave,name='update_employee_leave'),

    #                       leave requests

    path('add-leave-request',views.add_leave_request,name='add_leave_request'),
    #   pending
    path('update-leave-request/<str:id>', views.update_leave_request, name='update_leave_request'),
    path('delete-leave-request/<str:id>',views.delete_leave_request,name='delete_leave_request'),

    path('leave-history-list/<str:id>',views.leave_history_list,name='leave_history_list'),
    path('add-extra-leave/<str:id>',views.add_extra_leave,name='add_extra_leave'),



]