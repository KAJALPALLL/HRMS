import os
from django.shortcuts import render,redirect
from . models import Tickets,TicketConversation
from . forms import TicketForm
from user_management.models import Employee
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . filters import TicketsFilter
from django.core.paginator import Paginator
from task_management.models import TaskManagement, TaskConversation
from django.http import JsonResponse



@login_required(login_url='login')
def add_ticket(request):
    try:
        if request.method == "POST":
            form = TicketForm(request.POST,request.FILES)
            user_data = Employee.objects.filter(username=request.user).first()
            if form.is_valid:
                instance = form.save(commit=False)
                instance.client_id = user_data.id
                instance.save()
                messages.success(request,'Successfully added Ticket')
                return redirect('conversation',instance.id)
            else:
                messages.error(request,'Ticket not added')
                return redirect('add_ticket')
        else:
            form = TicketForm()
            return render(request,'add-ticket.html',{'form':form})
    except Exception as e:
        print(e)


# ticket list

@login_required(login_url='login')
def ticket_list(request):
    try:
        if request.user.is_superuser:
            ticket_data = Tickets.objects.all()
            filter = TicketsFilter(request.GET, queryset=ticket_data)
            data = filter.qs
            ticket_conversation_data = []
            for data in data:
                conv_data = TicketConversation.objects.filter(ticket_id=data.id).last()
                if conv_data:
                    if conv_data.employee_id:
                        message = 'employee'
                    elif conv_data.client_id:
                        message = 'client'
                else:
                    message = 'no msg'

                ticket_conversation_data.append({
                    'data':data,
                    'message':message
                })
            paginator = Paginator(ticket_conversation_data, 50)  # Show 25 contacts per page.

            page_number = request.GET.get("page")
            ticket_conversation = paginator.get_page(page_number)

            return render(request, 'ticket-list.html', {'ticket_conversation': ticket_conversation,'filter':filter})

        # employee

        elif Employee.objects.filter(username=request.user,groups__name='employee').first():
            employee_data = Employee.objects.filter(username=request.user).first()
            ticket_data = Tickets.objects.filter(department_id=employee_data.department_id).order_by('-id')
            filter = TicketsFilter(request.GET, queryset=ticket_data)
            data = filter.qs

            ticket_conversation_data = []

            for data in data:
                conv_data = TicketConversation.objects.filter(ticket_id=data.id).last()
                if conv_data:
                    if conv_data.employee_id == request.user.id:
                        message = 'awaited'
                    else:
                        message = 'replied'
                else:
                    message = 'no msg'
                ticket_conversation_data.append({
                    'message':message,
                    'data':data
                })
            paginator = Paginator(ticket_conversation_data, 20)  # Show 25 contacts per page.

            page_number = request.GET.get("page")
            ticket_conversation = paginator.get_page(page_number)

            return render(request, 'ticket-list.html', {'ticket_conversation':ticket_conversation,'filter':filter})

        elif Employee.objects.filter(username=request.user,groups__name='manager').first():
            employee_data = Employee.objects.filter(username=request.user).first()
            ticket_data = Tickets.objects.filter(department_id=employee_data.department_id)
            filter = TicketsFilter(request.GET, queryset=ticket_data)
            data = filter.qs

            ticket_conversation_data = []

            for data in data:
                conv_data = TicketConversation.objects.filter(ticket_id=data.id).last()
                if conv_data:
                    if conv_data.employee_id == request.user.id:
                        message = 'awaited'
                    else:
                        message = 'replied'
                else:
                    message = 'no msg'
                ticket_conversation_data.append({
                    'message':message,
                    'data':data
                })
            paginator = Paginator(ticket_conversation_data, 20)  # Show 25 contacts per page.

            page_number = request.GET.get("page")
            ticket_conversation = paginator.get_page(page_number)

            return render(request, 'ticket-list.html', {'ticket_conversation':ticket_conversation,'filter':filter})


        # client

        else:
            employee_data = Employee.objects.filter(username=request.user,groups__name='client').first()
            ticket_data = Tickets.objects.filter(client_id=employee_data.id)

            filter = TicketsFilter(request.GET, queryset=ticket_data)
            data = filter.qs
            ticket_conversation_data = []
            for ticket in data:
                conv_data = TicketConversation.objects.filter(ticket_id=ticket.id).last()
                if conv_data:
                    if conv_data.client_id == request.user.id:
                        message = 'awaited'
                    else:
                        message = 'replied'
                else:
                    message ='no msg'

                ticket_conversation_data.append({
                    'message': message,
                    'data':ticket
                })
            paginator = Paginator(ticket_conversation_data, 20)  # Show 25 contacts per page.

            page_number = request.GET.get("page")
            ticket_conversation = paginator.get_page(page_number)

            return render(request, 'ticket-list.html', {'ticket_conversation':ticket_conversation,'filter':filter})
    except Exception as e:
        print(e)
        return redirect('dashboard')

# ticket added by client

@login_required(login_url='login')
def client_add_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST,request.FILES)
        user_data = Employee.objects.filter(username=request.user).first()
        if form.is_valid:
            instance = form.save(commit=False)
            instance.client_id = user_data.id
            instance.save()
            return redirect('ticket_list')
        else:
            return redirect('client_add_ticket')
    else:

        form = TicketForm()
        return render(request,'client-add-ticket.html',{'form':form})


@login_required(login_url='login')
def update_ticket_status(request,id):
    if request.method == "POST":
        status = request.POST['status']
        ticket_data = Tickets.objects.filter(id=id).first()
        ticket_data.status = status
        ticket_data.save()
        messages.success(request,'Successfully updated status')
        return redirect('ticket_list')
    else:
        return redirect('ticket_list')



@login_required(login_url='login')
def conversation(request,id):
    ticket_data = Tickets.objects.filter(id=id).first()
    data = TicketConversation.objects.filter(ticket_id=id).order_by('id')
    return render(request,'conversation.html',{'id':id,'data':data,'ticket_data':ticket_data})




@login_required(login_url='login')
def delete_conversation(request,id,t_id):
    data = TicketConversation.objects.get(id=id)
    if data.image:
        os.remove(data.image.path)
    data.delete()
    messages.success(request,'Successfully deleted.')
    return redirect('conversation',t_id)


@login_required(login_url='login')
def add_conversation(request):
    if request.method == "POST":
        ticket_id = request.POST['ticket_id']
        mimetype = request.POST['mimetype']
        if mimetype == 'text':
            text = request.POST['text']
        else:
            image = request.FILES['image']

        if mimetype == 'text':

            employee_data = Employee.objects.filter(username=request.user,groups__name='employee').first()
            if employee_data:
                ticket_data = TicketConversation.objects.create(ticket_id=ticket_id,mimetype=mimetype,text=text,employee_id=employee_data.id)

            client_data = Employee.objects.filter(username=request.user,groups__name='client').first()
            if client_data:
                ticket_data = TicketConversation.objects.create(ticket_id=ticket_id,mimetype=mimetype,text=text,client_id=client_data.id)

            manager_data = Employee.objects.filter(username=request.user, groups__name='manager').first()
            if manager_data:
                ticket_data = TicketConversation.objects.create(ticket_id=ticket_id, mimetype=mimetype, text=text,
                                                                employee_id=manager_data.id)

            if request.user.is_superuser:
                ticket_data = TicketConversation.objects.create(ticket_id=ticket_id,mimetype=mimetype,text=text,employee_id=request.user.id)

        else:
            employee_data = Employee.objects.filter(username=request.user, groups__name='employee').first()
            if employee_data:
                ticket_data = TicketConversation.objects.create(ticket_id=ticket_id, mimetype=mimetype,image=image,
                                                                employee_id=employee_data.id)

            client_data = Employee.objects.filter(username=request.user, groups__name='client').first()
            if client_data:
                ticket_data = TicketConversation.objects.create(ticket_id=ticket_id, mimetype=mimetype,image=image,
                                                                client_id=client_data.id)

            manager_data = Employee.objects.filter(username=request.user, groups__name='manager').first()
            if manager_data:
                ticket_data = TicketConversation.objects.create(ticket_id=ticket_id, mimetype=mimetype, image=image,
                                                                employee_id=manager_data.id)

            if request.user.is_superuser:
                ticket_data = TicketConversation.objects.create(ticket_id=ticket_id,mimetype=mimetype,image=image,employee_id=request.user.id)

        return redirect('conversation',ticket_id)


@login_required(login_url='login')
def client_tickets(request,id,dep_id):
    ticket_data = Tickets.objects.filter(client_id=id,department_id=dep_id)

    ticket_conversation = []

    for data in ticket_data:
        conv_data = TicketConversation.objects.filter(ticket_id=data.id).last()
        if conv_data:
            if conv_data.client_id:
                message = 'client'
            else:
                message = 'employee'
        else:
            message = 'no msg'
        ticket_conversation.append({
            'data': data,
            'message':message
        })

    return render(request,'ticket-list.html',{'ticket_conversation':ticket_conversation})


@login_required(login_url='login')
def open_tickets(request):
    if request.user.is_superuser:
        ticket_data = Tickets.objects.filter(status='open')
        filter = TicketsFilter(request.GET, queryset=ticket_data)
        open_ticket = filter.qs

        ticket_conversation_data = []
        for data in open_ticket:
            conv_data = TicketConversation.objects.filter(ticket_id=data.id).last()
            if conv_data:
                if conv_data.employee_id == request.user.id:
                    message = 'employee'
                else:
                    message = 'client'
            else:
                message = 'no msg'
            ticket_conversation_data.append({
                'data':data,
                'message': message
            })

        filtered_data = Paginator(ticket_conversation_data, 2)
        page_num = request.GET.get('page')
        ticket_conversation = filtered_data.get_page(page_num)

        return render(request,'ticket-list.html',{'ticket_conversation':ticket_conversation,'filter':filter})

    # employee

    elif Employee.objects.filter(groups__name='employee',username=request.user):
        employee_data = Employee.objects.filter(groups__name='employee',username=request.user).first()
        ticket_data = Tickets.objects.filter(status='open',department_id=employee_data.department_id)

        filter = TicketsFilter(request.GET, queryset=ticket_data)
        open_ticket = filter.qs

        ticket_conversation_data = []

        for data in open_ticket:
            conv_data = TicketConversation.objects.filter(ticket_id=data.id).last()
            if conv_data:
                if conv_data.employee_id == request.user.id:
                    message = 'awaited'
                else:
                    message = 'replied'
            else:
                message = 'no msg'
            ticket_conversation_data.append({
                'data':data,
                'message':message

            })
        filtered_data = Paginator(ticket_conversation_data, 2)
        page_num = request.GET.get('page')
        ticket_conversation = filtered_data.get_page(page_num)

        return render(request,'ticket-list.html',{'ticket_conversation':ticket_conversation,'filter':filter})


    elif Employee.objects.filter(groups__name='manager',username=request.user):
        employee_data = Employee.objects.filter(groups__name='manager',username=request.user).first()
        ticket_data = Tickets.objects.filter(status='open',department_id=employee_data.department_id)

        filter = TicketsFilter(request.GET, queryset=ticket_data)
        open_ticket = filter.qs

        ticket_conversation_data = []

        for data in open_ticket:
            conv_data = TicketConversation.objects.filter(ticket_id=data.id).last()
            if conv_data:
                if conv_data.employee_id == request.user.id:
                    message = 'awaited'
                else:
                    message = 'replied'
            else:
                message = 'no msg'
            ticket_conversation_data.append({
                'data': data,
                'message': message

            })
        filtered_data = Paginator(ticket_conversation_data, 2)
        page_num = request.GET.get('page')
        ticket_conversation = filtered_data.get_page(page_num)

        return render(request,'ticket-list.html',{'ticket_conversation':ticket_conversation,'filter':filter})

    # client

    else:
        client_data = Employee.objects.filter(groups__name='client', username=request.user).first()
        ticket_data = Tickets.objects.filter(status='open', client_id=client_data.id)

        filter = TicketsFilter(request.GET, queryset=ticket_data)
        open_ticket = filter.qs

        ticket_conversation_data = []

        for data in open_ticket:
            conv_data = TicketConversation.objects.filter(ticket_id= data.id).last()
            if conv_data:
                if conv_data.client_id == request.user.id:
                    message = 'awaited'
                else:
                    message = 'replied'
            else:
                message = 'no msg'
            ticket_conversation_data.append({
                'data':data,
                'message':message
            })
        filtered_data = Paginator(ticket_conversation_data, 2)
        page_num = request.GET.get('page')
        ticket_conversation = filtered_data.get_page(page_num)

        return render(request,'ticket-list.html',{'ticket_conversation':ticket_conversation,'filter':filter})


@login_required(login_url='login')
def closed_tickets(request):

    if request.user.is_superuser:
        ticket_data = Tickets.objects.filter(status='close')

        filter = TicketsFilter(request.GET, queryset=ticket_data)
        close_ticket = filter.qs

        ticket_conversation_data = []

        for data in close_ticket:
            conv = TicketConversation.objects.filter(ticket_id=data.id).last()
            if conv:
                if conv.client_id:
                    message = 'client'
                else:
                    message = 'employee'
            else:
                message = 'no msg'
            ticket_conversation_data.append({
                'data': data,
                'message': message
            })

        filtered_data = Paginator(ticket_conversation_data, 2)
        page_num = request.GET.get('page')
        ticket_conversation = filtered_data.get_page(page_num)

        return render(request,'ticket-list.html',{'ticket_conversation':ticket_conversation,'filter':filter})

    # employee


    elif Employee.objects.filter(username=request.user,groups__name='employee').first():
        employee_data = Employee.objects.filter(groups__name='employee',username=request.user).first()

        ticket_data = Tickets.objects.filter(status='close',department_id=employee_data.department_id)

        filter = TicketsFilter(request.GET, queryset=ticket_data)
        close_ticket = filter.qs

        ticket_conversation_data = []
        for data in close_ticket:
            conv = TicketConversation.objects.filter(ticket_id=data.id).last()

            if conv:
                if conv.client_id == request.user.id:
                    message = 'awaited'
                else:
                    message = 'replied'
            else:
                message = 'no msg'
            ticket_conversation_data.append({
                'data':data,
                'message': message
            })
        filtered_data = Paginator(ticket_conversation_data, 2)
        page_num = request.GET.get('page')
        ticket_conversation = filtered_data.get_page(page_num)

        return render(request,'ticket-list.html',{'ticket_conversation':ticket_conversation,'filter':filter})


    elif Employee.objects.filter(username=request.user,groups__name='manager').first():
        employee_data = Employee.objects.filter(groups__name='manager',username=request.user).first()

        ticket_data = Tickets.objects.filter(status='close',department_id=employee_data.department_id)

        filter = TicketsFilter(request.GET, queryset=ticket_data)
        close_ticket = filter.qs

        ticket_conversation_data = []
        for data in close_ticket:
            conv = TicketConversation.objects.filter(ticket_id=data.id).last()

            if conv:
                if conv.client_id == request.user.id:
                    message = 'awaited'
                else:
                    message = 'replied'
            else:
                message = 'no msg'
            ticket_conversation_data.append({
                'data':data,
                'message': message
            })
        filtered_data = Paginator(ticket_conversation_data, 2)
        page_num = request.GET.get('page')
        ticket_conversation = filtered_data.get_page(page_num)

        return render(request,'ticket-list.html',{'ticket_conversation':ticket_conversation,'filter':filter})

    # client

    else:
        client_data = Employee.objects.filter(groups__name='client', username=request.user).first()

        ticket_data = Tickets.objects.filter(status='close',client_id=client_data.id)
        filter = TicketsFilter(request.GET, queryset=ticket_data)
        closed_ticket = filter.qs

        ticket_conversation_data = []

        for data in closed_ticket:
            conv_data = TicketConversation.objects.filter(ticket_id=data.id).last()

            if conv_data:
                if conv_data.client_id == request.user.id:
                    message = 'awaited'
                else:
                    message = 'replied'
            else:
                message = 'no msg'
            ticket_conversation_data.append({
                'message':message,
                'data': data
            })
        filtered_data = Paginator(ticket_conversation_data, 2)
        page_num = request.GET.get('page')
        ticket_conversation = filtered_data.get_page(page_num)

        return render(request,'ticket-list.html',{'ticket_conversation':ticket_conversation,'filter':filter})



@login_required(login_url='login')
def update_ticket(request,id):
    ticket_data = Tickets.objects.filter(id=id).first()
    if request.method == "POST":
        form = TicketForm(request.POST,request.FILES,instance=ticket_data)
        new_image = request.FILES.get('image')

        if new_image and ticket_data.image:
            os.remove(ticket_data.image.path)
            ticket_data.image = new_image

        if form.is_valid:
            form.save()
            messages.success(request,'Successfully updated Ticket')
            return redirect('ticket_list')
        else:
            messages.error(request,'Ticket not updated')
            return redirect('update_ticket',id)
    else:
        form = TicketForm(instance=ticket_data)
        return render(request,'update-tickets.html',{'data':ticket_data,'form':form})

@login_required(login_url='login')
def delete_ticket(request,id):
    data = Tickets.objects.filter(id=id).first()
    if data.image:
        os.remove(data.image.path)
    data.delete()
    messages.success(request,'Successfully deleted Ticket')
    return redirect('ticket_list')


@login_required(login_url='login')
def pip_data(request):
    try:
        ticket_data = Tickets.objects.filter(department_id=request.user.department_id,status='open')
        employee_data = Employee.objects.filter(username=request.user).first()
        task_data = TaskManagement.objects.filter(task_assign_to=employee_data,status='open')|TaskManagement.objects.filter(task_assign_from=employee_data,status='open')

        ticket = 0
        task = 0

        if employee_data.groups.filter(name='client').exists():
            ticket_data = Tickets.objects.filter(client_id=request.user.id, status='open')

            for tickets in ticket_data:
                conver_data = TicketConversation.objects.filter(ticket_id=tickets.id).last()

                if conver_data.employee_id == request.user.id:
                    ticket += 0
                elif conver_data.client_id == request.user.id:
                    ticket += 0
                else:
                    ticket += 1

            return JsonResponse({'tasks': None, 'tickets': ticket})


        for tickets in ticket_data:
            conver_data = TicketConversation.objects.filter(ticket_id=tickets.id).last()

            if conver_data.employee_id == request.user.id:
                ticket += 0
            elif conver_data.client_id == request.user.id:
                ticket += 0
            else:
                ticket += 1

        for tasks in task_data:
            conv_data = TaskConversation.objects.filter(task_id=tasks.id).last()
            if conv_data.message_by == request.user.id:
                task += 0
            else:
                task += 1

        return JsonResponse({'tasks': task, 'tickets': ticket})


    except Exception as e:
        return redirect('ticket_list')
