from django.shortcuts import render,redirect
from . models import Employee,EmployeeDocument,Department
from django.contrib import auth
from django.contrib.auth import authenticate
from . forms import EmployeeForm,EmployeeDocumentForm
from leave.models import LeaveType,EmployeeLeave,LeaveHistory,LeaveRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from datetime import datetime
import os,csv
from django.db.models import Sum
from django.contrib.auth.models import Group
from ticketing_support.models import Tickets


# employee,created = Group.objects.get_or_create(name='employee')
# client,created = Group.objects.get_or_create(name='client')
# manager,created = Group.objects.get_or_create(name='manager')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            employee_data = Employee.objects.filter(username=request.user).first()
            if not employee_data.is_superuser:

                request.session['image'] = f'media/{employee_data.profile_image}'
            else:
                print('hello')

            messages.success(request,'Successfully Logged In')
            return redirect('dashboard')

        else:
            messages.error(request,'Register Yourself !!!')
            return redirect('register')
    else:
        return render(request,'login.html')





@login_required(login_url='login')
def add_employee(request):
    try:
        if request.method == "POST":
            form = EmployeeForm(request.POST,request.FILES)
            is_active = request.POST['is_active']
            email = request.POST['email']
            password = request.POST['password']
            name = request.POST['name']
            manager = request.POST.get('manager')

            if manager:

                if form.is_valid:
                    instance = form.save(commit=False)
                    instance.is_active = is_active
                    instance.username = email
                    instance.email = email
                    instance.first_name = name
                    instance.set_password(password)
                    instance.save()


                    group = Group.objects.get(name='manager')
                    group_data = instance.groups.add(group)
                    group.save()

                    leave_data = LeaveType.objects.all()
                    # Leave type mapping with the employee ( EMployeeLeave )
                    # Leave History Created..

                    for data in leave_data:

                        employee_name = Employee.objects.filter(username=email).first()
                        admin_data = Employee.objects.filter(username=request.user).first()
                        employee_leave_data = EmployeeLeave.objects.create(leave_type_id=data.id,employee_id=employee_name.id,values=data.value,status='pending')
                        employee_leave_data.save()
                        leave_history_data = LeaveHistory.objects.create(employee_leave_type_id=employee_leave_data.id,
                                                                         description=data.name,
                                                                         added_by_id=admin_data.id, status='credit',
                                                                         value=data.value)
                        leave_history_data.save()

                    messages.success(request,'Successfully Added Employee data')
                    return redirect('employee_list')
                else:
                    messages.error(request,'Not Added')
                    return redirect('add_employee')
            else:

                if form.is_valid:
                    instance = form.save(commit=False)
                    instance.is_active = is_active
                    instance.username = email
                    instance.email = email
                    instance.first_name = name

                    instance.set_password(password)
                    instance.save()

                    group = Group.objects.get(name='employee')
                    group_data = instance.groups.add(group)
                    group.save()

                    leave_data = LeaveType.objects.all()
                    # Leave type mapping with the employee ( EMployeeLeave )
                    # Leave History Created..

                    for data in leave_data:
                        employee_name = Employee.objects.filter(username=email).first()
                        admin_data = Employee.objects.filter(username=request.user).first()
                        employee_leave_data = EmployeeLeave.objects.create(leave_type_id=data.id,
                                                                           employee_id=employee_name.id,
                                                                           values=data.value, status='pending')
                        employee_leave_data.save()
                        leave_history_data = LeaveHistory.objects.create(employee_leave_type_id=employee_leave_data.id,
                                                                         description=data.name,
                                                                         added_by_id=admin_data.id, status='credit',
                                                                         value=data.value)
                        leave_history_data.save()

                    messages.success(request, 'Successfully Added Employee data')
                    return redirect('employee_list')
                else:
                    messages.error(request, 'Not Added')
                    return redirect('add_employee')


        else:
            form = EmployeeForm
            return render(request,'add-employee.html',{'form':form})
    except Exception as e:
        print(e)


# Pagination
@login_required(login_url='login')
def employee_list(request):
    employee_data = Employee.objects.filter(groups__name = 'employee').order_by('-id') | Employee.objects.filter(groups__name = 'manager').order_by('-id')
    filtered_data = Paginator(employee_data,50)
    page_num = request.GET.get('page')
    data = filtered_data.get_page(page_num)
    return render(request,'employee-list.html',{'data':data})


#                                       Images delete
@login_required(login_url='login')
def update_employee(request,id):
    employee_data = Employee.objects.get(id=id)
    if request.method == "POST":

        form = EmployeeForm(request.POST,request.FILES,instance=employee_data)
        is_active = request.POST['is_active']
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']

        new_profile_image = request.FILES.get('profile_image')
        if employee_data.profile_image and new_profile_image:
            os.remove(employee_data.profile_image.path)
            employee_data.profile_image = new_profile_image

        if form.is_valid:

            instance = form.save(commit=False)
            if is_active:
                instance.is_active = is_active
            else:
                instance.is_active = employee_data.is_active
            if email:
                instance.email = email
            else:
                instance.email = employee_data.email

            if password:
                instance.set_password(password)

            if name:
                instance.username = email
            else:
                instance.username = employee_data.username
            instance.save()

            messages.success(request,'Successfully updated Employee data')
            return redirect('employee_list')
        else:
            messages.error(request,'Not Updated')
            return redirect('update_employee',id)
    else:
        form = EmployeeForm(instance=employee_data)
        return render(request,'update-employee.html',{'form':form,'employee_data':employee_data})


@login_required(login_url='login')
def delete_employee(request,id):
    data = Employee.objects.filter(id=id).first()
    if data.profile_image:
        os.remove(data.profile_image.path)

    data.delete()
    messages.success(request,'Successfully Deleted Employee Data')
    return redirect('employee_list')




@login_required(login_url='login')
def my_leave_list(request):
    data = EmployeeLeave.objects.filter(employee_id__username=request.user)
    return render(request,'employee-leave-list.html',{'data':data})


@login_required(login_url='login')
def my_profile(request):
    data = Employee.objects.filter(username=request.user).first()
    return render(request,'profile.html',{'data':data})

@login_required(login_url='login')
def my_document(request):
    data = EmployeeDocument.objects.filter(employee_id__username=request.user)
    return render(request,'my-documents.html',{'data':data})




def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def add_employee_document(request):
    if request.method == "POST":
        form = EmployeeDocumentForm(request.POST,request.FILES)
        if form.is_valid:
            form.save()
            return redirect('documents_list')
        else:
            return redirect('documents_list')
    else:
        form = EmployeeDocumentForm()
        return render(request,'add-employee-document.html',{'form':form})





def register(request):
    try:
        if request.method == "POST":
            form = EmployeeForm(request.POST,request.FILES)
            email = request.POST['email']
            password = request.POST['password']
            name = request.POST['name']

            if form.is_valid:
                instance = form.save(commit=False)
                instance.email = email
                instance.set_password(password)
                instance.username = email
                instance.first_name = name
                instance.is_active = True
                instance.save()

                group = Group.objects.get(name='employee')
                group_data = instance.groups.add(group)
                group.save()



                leave_data = LeaveType.objects.all()
                # Leave type mapping with the employee ( EMployeeLeave )
                # Leave History Created..

                for data in leave_data:
                    employee_name = Employee.objects.filter(username=email).first()
                    admin_data = Employee.objects.filter(is_superuser=True).first()
                    employee_leave_data = EmployeeLeave.objects.create(leave_type_id=data.id,
                                                                       employee_id=employee_name.id, values=data.value,
                                                                       status='pending')
                    employee_leave_data.save()
                    leave_history_data = LeaveHistory.objects.create(employee_leave_type_id=employee_leave_data.id,
                                                                     description=data.name,
                                                                     added_by_id=admin_data.id, status='credit',
                                                                     value=data.value)
                    leave_history_data.save()

                return redirect('login')
            else:
                messages.error(request,'Data Not Valid')
                return redirect('register')
        else:
            form = EmployeeForm()
            return render(request,'register.html',{'form':form})
    except Exception as e:
        print(e)

@login_required(login_url='login')
def employee_leave_list(request,id):
    data = EmployeeLeave.objects.filter(employee_id=id)
    return render(request,'employee-leave-list.html',{'data':data,'id':id})


@login_required(login_url='login')
def add_documents(request):
    if request.method == "POST":
        form = EmployeeDocumentForm(request.POST,request.FILES)
        employee_id = request.POST['employee']
        if form.is_valid:
            employee_data = Employee.objects.filter(username=employee_id).first()
            instance = form.save(commit=False)
            instance.employee_id = employee_data.id
            instance.save()
            messages.success(request,'Successfully added Documents')
            return redirect('documents_list')
        else:
            messages.error(request,'Not Added')
            return redirect('add_documents')
    else:
        form = EmployeeDocumentForm()
        return render(request,'add-employee-document.html',{'form':form})


@login_required(login_url='login')
def documents_list(request):
    employee_data = request.user
    user_data = Employee.objects.filter(username=employee_data).first()
    data = EmployeeDocument.objects.filter(employee_id=user_data.id)
    return render(request,'my-documents.html',{'data':data})

@login_required(login_url='login')
def employee_document_list(request,id):
    user_data = Employee.objects.filter(id=id).first()
    data = EmployeeDocument.objects.filter(employee_id=user_data.id)
    return render(request, 'my-documents.html', {'data': data})



@login_required(login_url='login')
def export_leave(request):
    starting_date = request.POST['start_date']
    ending_date = request.POST['end_date']

    start_date = datetime.strptime(starting_date,'%Y-%m-%d').date()
    end_date = datetime.strptime(ending_date,'%Y-%m-%d').date()

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition":'attachment;filename="employee-leave.csv"'},)

    # leave types

    leave_type_data = LeaveType.objects.all()

    leave_data = []
    for data in leave_type_data:
        leave_data.append(data.name)

    writer = csv.writer(response)
    row = ['Employee'] + leave_data
    writer.writerow(row)

    # employee list
    employee_data = Employee.objects.filter(is_superuser=False)

    for employee in employee_data:
        row = [employee.username]
        for leave_type in leave_type_data:
            data = LeaveRequest.objects.filter(status='approved',start_date__range=[start_date,end_date],employee_id=employee.id,leave_type_id=leave_type.id)

            if not data:
                row.append(0)
            else:
                num = float(0)
                for i in data:
                    # add same leave type days and also place them in correct cell
                    if i.leave_type_id == leave_type.id:
                        num += float(i.days)
                row.append(num)
        writer.writerow(row)

    return response




def client_register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user_data = Employee.objects.create_user(username=username,password=password)
        group = Group.objects.get(name='client')
        group_data = user_data.groups.add(group)
        user_data.save()
        return redirect('login')
    else:
        return render(request,'client-register.html')


@login_required(login_url='login')
def client_list(request):
    client_data = Employee.objects.filter(groups__name='client').order_by('-id')

    status_ticket = []
    for data in client_data:
        open_ticket = Tickets.objects.filter(client_id=data.id,status='open').count()
        open_ticket_data = open_ticket
        closed_ticket = Tickets.objects.filter(client_id=data.id,status='close').count()
        closed_ticket_data = closed_ticket

        status_ticket.append({
            'closed_ticket': closed_ticket,
            'open_ticket':open_ticket,
            'data': data
        })

    paginator = Paginator(status_ticket,50)

    page_number = request.GET.get("page")
    status_ticket_list = paginator.get_page(page_number)

    return render(request,'client-list.html',{'status_ticket_list':status_ticket_list})




@login_required(login_url='login')
def select_department(request,id):
    department_data = Department.objects.all()
    employee_data = Employee.objects.filter(groups__name='client',id=id)

    department_status_data = []
    for data in department_data:
        open_ticket_data = Tickets.objects.filter(client_id=id,department_id=data.id,status='open').count()

        closed_ticket_data = Tickets.objects.filter(client_id=id,department_id=data.id,status='close').count()

        department_status_data.append({
            'data': data,
            'open_status': open_ticket_data,
            'close_status' :closed_ticket_data
        })
    return render(request,'department.html',{'department_status_data':department_status_data,'id':id})


@login_required(login_url='login')
def export_client_report(request,id):

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment;filename="Client-Ticket.csv"'}, )

    client_data = Employee.objects.filter(id=id).first()

    open_ticket = Tickets.objects.filter(client_id=client_data.id,status='open').count()
    closed_ticket = Tickets.objects.filter(client_id=client_data.id,status='close').count()


    writer = csv.writer(response)

    writer.writerow(['Client name','Open Ticket','Closed Ticket'])

    row = [client_data.username] + [open_ticket] + [closed_ticket]
    writer.writerow(row)
    return response





