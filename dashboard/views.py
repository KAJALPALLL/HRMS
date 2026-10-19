from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from user_management.models import Employee
from django.contrib.auth.decorators import login_required
from leave.models import LeaveType,LeaveRequest,EmployeeLeave
from ticketing_support.models import Tickets
from task_management.models import TaskManagement


@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        employee_data = Employee.objects.filter(is_superuser=False).count()
        leave_type = LeaveType.objects.all().count()
        pending_leave_request = LeaveRequest.objects.filter(status='pending').count()
        approved_leave_request = LeaveRequest.objects.filter(status='approved').count()
        rejected_leave_request = LeaveRequest.objects.filter(status='rejected').count()
        open_ticket_data = Tickets.objects.filter(status='open').count()
        closed_ticket_data = Tickets.objects.filter(status='close').count()
        open_task_data = TaskManagement.objects.filter(status='open').count()
        closed_task_data = TaskManagement.objects.filter(status='close').count()
        return render(request, 'dashboard.html', {'employee_data': employee_data,
                                                  'leave_type': leave_type,'open_ticket_data':open_ticket_data,
                                                  'closed_ticket_data':closed_ticket_data,
                                                  'pending_leave_request': pending_leave_request,
                                                  'approved_leave_request': approved_leave_request,
                                                  'rejected_leave_request': rejected_leave_request,
                                                  'open_task_data':open_task_data,
                                                  'closed_task_data':closed_task_data
                                                  })


    elif Employee.objects.filter(username=request.user,groups__name='employee').first():
        employee_data = Employee.objects.filter(username=request.user,groups__name='employee').first()
        pending_leave_request = LeaveRequest.objects.filter(employee_id=employee_data.id,status='pending').count()
        approved_leave_request = LeaveRequest.objects.filter(employee_id=employee_data.id, status='approved').count()
        rejected_leave_request = LeaveRequest.objects.filter(employee_id=employee_data.id, status='rejected').count()
        open_ticket_data = Tickets.objects.filter(department_id=employee_data.department_id,status='open').count()
        closed_ticket_data = Tickets.objects.filter(department_id=employee_data.department_id,status='close').count()
        open_task_data = TaskManagement.objects.filter(task_assign_from=employee_data,status='open')| TaskManagement.objects.filter(task_assign_to=employee_data,status='open')
        open_ticket = 0
        for open in open_task_data:
            open_ticket += 1
        close_ticket = 0
        close_task_data = TaskManagement.objects.filter(task_assign_from=employee_data,status='close')| TaskManagement.objects.filter(task_assign_to=employee_data,status='close')
        for close in close_task_data:
            close_ticket += 1

        return render(request,'dashboard.html',
                                            {'pending_leave_request':pending_leave_request,
                                            'rejected_leave_request':rejected_leave_request,
                                            'approved_leave_request':approved_leave_request,'employee_data':employee_data,
                                            'open_ticket_data':open_ticket_data,
                                             'closed_ticket_data':closed_ticket_data,
                                             'open_task_data':open_ticket,
                                             'close_task_data':close_ticket
                                             })

    elif Employee.objects.filter(username=request.user, groups__name='manager').first():
        employee_data = Employee.objects.filter(username=request.user, groups__name='manager').first()
        pending_leave_request = LeaveRequest.objects.filter(employee_id=employee_data.id, status='pending').count()
        approved_leave_request = LeaveRequest.objects.filter(employee_id=employee_data.id, status='approved').count()
        rejected_leave_request = LeaveRequest.objects.filter(employee_id=employee_data.id, status='rejected').count()
        open_ticket_data = Tickets.objects.filter(department_id=employee_data.department_id, status='open').count()
        closed_ticket_data = Tickets.objects.filter(department_id=employee_data.department_id, status='close').count()
        open_task_data = TaskManagement.objects.filter(task_assign_from=employee_data,
                                                       status='open') | TaskManagement.objects.filter(
            task_assign_to=employee_data, status='open')
        open_ticket = 0
        for open in open_task_data:
            open_ticket += 1
        close_ticket = 0
        close_task_data = TaskManagement.objects.filter(task_assign_from=employee_data,
                                                        status='close') | TaskManagement.objects.filter(
            task_assign_to=employee_data, status='close')
        for close in close_task_data:
            close_ticket += 1

        return render(request, 'dashboard.html',
                                              {'pending_leave_request': pending_leave_request,
                                               'rejected_leave_request': rejected_leave_request,
                                               'approved_leave_request': approved_leave_request, 'employee_data': employee_data,
                                               'open_ticket_data': open_ticket_data, 'closed_ticket_data': closed_ticket_data})

    else:
        open_ticket_data = Tickets.objects.filter(client_id=request.user.id,status='open').count()
        close_ticket_data = Tickets.objects.filter(client_id=request.user.id,status='close').count()
        return render(request,'dashboard.html',{'open_ticket_data':open_ticket_data,'close_ticket_data':close_ticket_data})



@login_required(login_url='login')
def rules(request):
    return render(request,'rules.html')


@login_required(login_url='login')
def client_rules(request):
    return render(request,'client-rules.html')