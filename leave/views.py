import datetime

from django.shortcuts import render,redirect
from . models import LeaveType,LeaveRequest,EmployeeLeave,LeaveHistory
from . forms import LeaveTypeForm,UpadteLeaveRequestForm,LeaveHistoryForm
from user_management.models import Employee,Department
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from . filters import LeaveFilters
from datetime import timedelta,date,datetime


@login_required(login_url='login')
def add_leave_type(request):
    try:
        if request.method == "POST":
            form = LeaveTypeForm(request.POST)
            if form.is_valid:
                instance = form.save(commit=False)

                # if it does not exist ( then add condition )

                if instance.name == 'Leave Without Pay':
                    messages.error(request,'It already Exist')
                    return redirect('leave_list')
                else:
                    instance.save()

                # mapping with every employee
                    leave_type_data = LeaveType.objects.filter(id=instance.id).first()
                    employee_data = Employee.objects.filter(is_superuser=False)
                    user_data = Employee.objects.filter(username=request.user).first()

                    paid_leave, created = LeaveType.objects.get_or_create(name='Leave Without Pay', value=0)
                    if created:
                        for data in employee_data:
                            employee_leave_data = EmployeeLeave.objects.create(leave_type_id=paid_leave.id,
                                                                               employee_id=data.id, status='pending',
                                                                               values=paid_leave.value)
                            leave_history_data = LeaveHistory.objects.create(employee_leave_type_id=employee_leave_data.id,
                                                                             description=paid_leave.name, added_by_id=user_data.id,
                                                                             status='credited', value=paid_leave.value)

                    for data in employee_data:
                        employee_leave_data = EmployeeLeave.objects.create(leave_type_id=leave_type_data.id,employee_id=data.id,status='pending',values=leave_type_data.value)
                        leave_history_data = LeaveHistory.objects.create(employee_leave_type_id=employee_leave_data.id, description=instance.name,added_by_id=user_data.id,status='credited',value=instance.value)

                    messages.success(request,'Successfully Added Leave Type')
                    return redirect('leave_list')
            else:
                messages.error(request,'Not Added')
                return redirect('add_leave_type')
        else:
            form = LeaveTypeForm()
            return render(request,'add-leave-type.html',{'form':form})
    except Exception as e:
        return redirect('dashboard')

@login_required(login_url='login')
def leave_list(request):
    leave_data = LeaveType.objects.all().order_by('-id')
    paginator = Paginator(leave_data, 50)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    return render(request,'leave-list.html',{'data':data})


@login_required(login_url='login')
def update_leave_type(request,id):
    try:
        leave_data = LeaveType.objects.get(id=id)
        if request.method == "POST":
            form = LeaveTypeForm(request.POST,instance=leave_data)
            if form.is_valid:
                form.save()
                messages.success(request,'Successfully Updated Leave Type')
                return redirect('leave_list')
            else:
                messages.error(request,'Not Updated')
                return render(redirect,'update_leave_type',id)
        else:
            form = LeaveTypeForm(instance=leave_data)
            return render(request,'update-leave-type.html',{'form':form})
    except Exception as e:
        return redirect('dashboard')

@login_required(login_url='login')
def delete_leave_type(request,id):
    data = LeaveType.objects.filter(id=id)
    data.delete()
    messages.success(request,'Successfully Deleted Leave Type')
    return redirect('leave_list')



# update the values

@login_required(login_url='login')
def add_leave_request(request):
    if request.method == "POST":
        day_type = request.POST['day_type']
        employee = request.POST['employee']
        leave_type = request.POST['leave_type']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        leave_reason = request.POST['leave_reason']

        starting_date = datetime.strptime(start_date,'%Y-%m-%d').date()
        ending_date = datetime.strptime(end_date,'%Y-%m-%d').date()
        days = (ending_date-starting_date).days

        data = Employee.objects.filter(username=employee).first()
        employee_data = data.id
        leave_type_id = LeaveType.objects.filter(id=leave_type).first()

        if leave_type_id.name == 'Leave Without Pay':
            if day_type == 'full day':

                paid_leave_apply = LeaveRequest.objects.create(employee_id=employee_data, leave_type_id=leave_type,
                                                                  start_date=start_date, end_date=end_date,
                                                                  leave_reason=leave_reason, days=float(days+1),
                                                                  day_type='full day')
            else:
                paid_leave_apply = LeaveRequest.objects.create(employee_id=employee_data, leave_type_id=leave_type,
                                                               start_date=start_date, end_date=end_date,
                                                               leave_reason=leave_reason, days=float(days +0.5),
                                                               day_type='half day')
            messages.success(request,'Successfully applied for Leave Without Pay')
            return redirect('my_leave_request')

        leave_request_data = LeaveRequest.objects.filter(employee_id=employee_data,start_date__range=[starting_date,end_date])
        remaining_data = LeaveRequest.objects.filter(employee_id=employee_data,leave_type_id=leave_type,status='pending' or 'approved')
        remain_data = float(0)
        for data in remaining_data:
            remain_data += float(data.days)
        if leave_request_data:
            messages.error(request,'You are already on a leave !!!')
            return redirect('my_leave_request')
        else:

            per_employee_leave_data = EmployeeLeave.objects.filter(employee_id=employee_data,leave_type_id=leave_type).first()

            if float(remain_data) < float(per_employee_leave_data.values):
                print(remain_data,per_employee_leave_data.values)
                if day_type == 'full day':

                    if float(days+remain_data+1) <= float(per_employee_leave_data.values):
                        print(days+remain_data+1,per_employee_leave_data.values)
                        leave_request_apply = LeaveRequest.objects.create(employee_id=employee_data,leave_type_id=leave_type,start_date=start_date,end_date=end_date,leave_reason=leave_reason,days=float(days+1),day_type='full day')
                        leave_request_apply.save()
                        messages.success(request, 'Successfully Requested for a leave')
                        return redirect('my_leave_request')
                    else:
                        messages.success(request, 'Leaves are not Left ')
                        return redirect('my_leave_request')

                else:
                    if float(days)+0.5 <= float(per_employee_leave_data.values):

                        leave_request_apply = LeaveRequest.objects.create(employee_id=employee_data,leave_type_id=leave_type,start_date=start_date,end_date=end_date,leave_reason=leave_reason,days=float(days+0.5),day_type='half day')
                        leave_request_apply.save()
                        messages.success(request,'Successfully Requested for a leave')
                        return redirect('my_leave_request')
                    else:
                        messages.success(request, 'Leaves are not Left ')
                        return redirect('my_leave_request')
            else:
                messages.success(request, 'Leaves are not Left ')
                return redirect('my_leave_request')
    else:
        leave_type_data = LeaveType.objects.all()
        return render(request,'add-leave-request.html',{'leave_type_data':leave_type_data})



@login_required(login_url='login')
def leave_request_list(request):
    leave_data = LeaveRequest.objects.all().order_by('-id')
    filter = LeaveFilters(request.GET,queryset = leave_data)
    filtered_data = filter.qs
    paginator = Paginator(filtered_data,50)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)

    return render(request, 'leave-request-list.html', {'data': data,'filter':filter})





@login_required(login_url='login')
def update_leave_request(request,id):
    leave_apply_data = LeaveRequest.objects.get(id=id)
    if request.method == "POST":
        form = UpadteLeaveRequestForm(request.POST,instance=leave_apply_data)

        if form.is_valid:
            instance = form.save(commit=False)
            starting_date = instance.start_date
            ending_date = instance.end_date

            days = (ending_date-starting_date).days
            instance.days = days
            instance.save()

            messages.success(request,'Successfully Updated Request for a Leave')
            return redirect('leave_request_list')
        else:
            messages.error(request,'Not updated ')
            return redirect('update_leave_request',id)
    else:
        form = UpadteLeaveRequestForm(instance=leave_apply_data)
        return render(request,'update-leave-request.html',{'form':form})


@login_required(login_url='login')
def delete_leave_request(request,id):
    data = LeaveRequest.objects.filter(id=id)
    data.delete()
    messages.success(request,'Successfully Delete Leave Request')
    return redirect('leave_request_list')




@login_required(login_url='login')
def update_leave_request_status(request,id):
    try:

        leave_request_data = LeaveRequest.objects.filter(id=id).first()
        employee_data = Employee.objects.filter(username=request.user).first()

        if request.method == 'POST':
            status = request.POST['status']
            leave_request_data.status = status
            if leave_request_data.status == 'approved':
                leave_type_id = LeaveType.objects.filter(id=leave_request_data.leave_type_id).first()
                if leave_type_id.name == 'Leave Without Pay':
                    employee_leave_data = EmployeeLeave.objects.filter(leave_type_id=leave_request_data.leave_type_id,
                                                                       employee_id=leave_request_data.employee_id).first()
                    employee_leave_data.save()
                    history_data = LeaveHistory.objects.create(employee_leave_type_id=employee_leave_data.id,
                                                               description=leave_request_data.status,
                                                               value=leave_request_data.days, status='deducted',
                                                               added_by_id=employee_data.id)
                    history_data.save()
                else:
                    employee_leave_data = EmployeeLeave.objects.filter(leave_type_id=leave_request_data.leave_type_id,employee_id=leave_request_data.employee_id).first()
                    employee_leave_data.values = float(employee_leave_data.values) - float(leave_request_data.days)
                    employee_leave_data.save()
                    history_data = LeaveHistory.objects.create(employee_leave_type_id=employee_leave_data.id,description=leave_request_data.status,value=leave_request_data.days,status='deducted',added_by_id=employee_data.id)
                    history_data.save()

            leave_request_data.approved_by_id = employee_data.id
            leave_request_data.approved_date = date.today()
            leave_request_data.save()
            messages.success(request,'Updated Leave Request Status')
        return redirect('employee_list')
    except Exception as e:
        return redirect('dashboard')



@login_required(login_url='login')
def employee_leave_request(request,id):
    data = LeaveRequest.objects.filter(employee_id=id).order_by('-id')
    return render(request,'leave-request-list.html',{'data':data})


@login_required(login_url='login')
def update_employee_leave(request,id):
    data = EmployeeLeave.objects.filter(employee_id=id)
    return render(request,'update-employee-leave.html',{'data':data})


@login_required(login_url='login')
def my_leave_request(request):
    my_data = Employee.objects.filter(username=request.user).first()
    filtered_data = LeaveRequest.objects.filter(employee_id=my_data.id).order_by('-id')

    paginator = Paginator(filtered_data, 50)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)

    return render(request,'leave-request-list.html',{'data':data})



@login_required(login_url='login')
def leave_history_list(request,id):
    data = LeaveHistory.objects.filter(employee_leave_type_id=id)
    return render(request,'leave-history-list.html',{'data':data,'id':id})


@login_required(login_url='login')
def add_extra_leave(request,id):

    if request.method == "POST":
        form = LeaveHistoryForm(request.POST)
        if form.is_valid:
            instance = form.save(commit=False)
            employee_leave_data = EmployeeLeave.objects.filter(id=id).first()
            instance.employee_leave_type_id = employee_leave_data.id
            user_data = Employee.objects.filter(username=request.user).first()
            instance.added_by_id = user_data.id
            instance.status = 'credited'
            instance.save()
            add_employee_leave = EmployeeLeave.objects.filter(id=id).update(employee_id=employee_leave_data.employee_id,leave_type_id=employee_leave_data.leave_type_id,status='approved',values=float(employee_leave_data.values)+float(instance.value))

            return redirect('leave_history_list',id)
        else:
            return redirect('add_extra_leave',id)
    else:
        form = LeaveHistoryForm()
        return render(request,'add-extra-leave.html',{'form':form})




