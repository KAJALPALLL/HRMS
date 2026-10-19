import os
from django.shortcuts import render,redirect
from . models import TaskManagement,TaskConversation
from . forms import TaskForm
from . filters import TaskFilter
from user_management.models import Employee
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages



@login_required(login_url='login')
def add_task(request):
    if request.method == "POST":
        task_assign_to = request.POST.getlist('task_assign_to')
        task_assign_from = request.POST.getlist('task_assign_from')

        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task_data = form.save(commit=False)
            task_data.save()

            for assign_to in task_assign_to:
                employee_data = Employee.objects.filter(username=assign_to).first()
                if employee_data:
                    task_data.task_assign_to.add(employee_data)

            for assign_from in task_assign_from:
                manager_data = Employee.objects.filter(username=assign_from).first()
                if manager_data:
                    task_data.task_assign_from.add(manager_data)

            task_data.save()

            return redirect('task_conversation',task_data.id)
        else:
            return redirect('add_task')
    else:
        form = TaskForm()
        employee = Employee.objects.filter(groups__name='employee')|Employee.objects.filter(groups__name='manager')|Employee.objects.filter(is_superuser=True)
        return render(request, 'add-task.html', {'form': form,'employee':employee})


@login_required(login_url='login')
def task_list(request):
    data = TaskManagement.objects.all().order_by('-id')
    filter = TaskFilter(request.GET,queryset=data)
    task_data = filter.qs

    task_conversation_data = []

    for data in task_data:
        convo_data = TaskConversation.objects.filter(task_id=data.id).last()
        if convo_data:
            message = convo_data.message_by.username
        else:
            message = 'no msg'
        task_conversation_data.append({
            'data': data,
            'message':message
        })

    paginator = Paginator(task_conversation_data,20)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    conversation_data = paginator.get_page(page_number)

    return render(request,'tasks-list.html',{'data':task_data,'conversation_data':conversation_data,'filter':filter})


@login_required(login_url='login')
def update_task(request,id):
    task_data = TaskManagement.objects.filter(id=id).first()
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task_data)
        new_image = request.FILES.get('image')

        if new_image and task_data.image:
            os.remove(task_data.image.path)
            task_data.image = new_image

        if form.is_valid:
            form.save()
            messages.success(request, 'Successfully updated Task')
            return redirect('task_list')
        else:
            messages.error(request, 'Task not updated')
            return redirect('update_task', id)
    else:
        form = TaskForm(instance=task_data)
        return render(request,'update-task.html',{'form':form,'task_data':task_data})



@login_required(login_url='login')
def delete_task(request,id):
    task_data = TaskManagement.objects.filter(id=id).first()
    if task_data.image:
        os.remove(task_data.image.path)
    task_data.delete()
    return redirect('task_list')



@login_required(login_url='login')
def task_conversation(request,id):
    task_data = TaskManagement.objects.filter(id=id).first()
    conversation_data = TaskConversation.objects.filter(task_id=id)
    return render(request,'task-conversation.html',{'data':task_data,'conversation_data':conversation_data})



@login_required(login_url='login')
def employee_task_list(request):
    data = TaskManagement.objects.filter(task_assign_to=request.user)|TaskManagement.objects.filter(task_assign_from=request.user).order_by('-id')

    filter = TaskFilter(request.GET, queryset=data)
    task_data = filter.qs

    task_conversation_data = []

    for data in task_data:
        convo_data = TaskConversation.objects.filter(task_id=data.id).last()
        if convo_data:
            message = convo_data.message_by.username
        else:
            message = 'no msg'
        task_conversation_data.append({
            'data': data,
            'message': message
        })
    paginator = Paginator(task_conversation_data, 20)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    conversation_data = paginator.get_page(page_number)

    return render(request, 'tasks-list.html', {'data': task_data,'conversation_data':conversation_data,'filter':filter})


@login_required(login_url='login')
def task_status_update(request,id):
    if request.method == "POST":
        status = request.POST['status']
        task_data = TaskManagement.objects.filter(id=id)
        for i in task_data:
            i.status = status
            i.save()
            return redirect('employee_task_list')
    else:
        pass

@login_required(login_url='login')
def add_task_conversation(request):
    try:
        if request.method == "POST":
            task_id = request.POST['task_id']
            mimetype = request.POST['mimetype']
            if mimetype == 'text':

                text = request.POST['text']
            else:
                image = request.FILES['image']

            if mimetype == 'text':

                employee_data = Employee.objects.filter(username=request.user).first()
                if employee_data:
                    task_data = TaskConversation.objects.create(task_id=task_id,mimetype=mimetype,text=text,message_by_id=employee_data.id)
                    task_data.save()
                    return redirect('task_conversation', task_id)
                else:
                    return redirect('task_list')
            else:
                employee_data = Employee.objects.filter(username=request.user).first()
                if employee_data:
                    ticket_data = TaskConversation.objects.create(task_id=task_id, mimetype=mimetype,image=image,
                                                                    message_by_id=employee_data.id)
                    ticket_data.save()
                    return redirect('task_conversation',task_id)
                else:
                    return redirect('task_list')
        else:
            return redirect('task_list')

    except Exception as e:
        print(e)


@login_required(login_url='login')
def open_task_list(request):
    if request.user.is_superuser:
        task_data = TaskManagement.objects.filter(status='open')
        filter = TaskFilter(request.GET, queryset=task_data)
        data = filter.qs

        task_conversation_data = []

        for data in data:
            convo_data = TaskConversation.objects.filter(task_id=data.id).last()
            if convo_data:
                message = convo_data.message_by.username
            else:
                message = 'no msg'
            task_conversation_data.append({
                'data': data,
                'message': message
            })

        paginator = Paginator(task_conversation_data, 20)  # Show 25 contacts per page.
        page_number = request.GET.get("page")
        conversation_data = paginator.get_page(page_number)

        return render(request,'tasks-list.html',{'data':data,'conversation_data':conversation_data,'filter':filter})
    else:
        task_data = TaskManagement.objects.filter(task_assign_to=request.user,status='open')|TaskManagement.objects.filter(task_assign_from=request.user,status='open')

        filter = TaskFilter(request.GET, queryset=task_data)
        data = filter.qs

        task_conversation_data = []

        for data in data:
            convo_data = TaskConversation.objects.filter(task_id=data.id).last()
            if convo_data:
                message = convo_data.message_by.username
            else:
                message = 'no msg'
            task_conversation_data.append({
                'data': data,
                'message': message
            })

        paginator = Paginator(task_conversation_data, 20)  # Show 25 contacts per page.
        page_number = request.GET.get("page")
        conversation_data = paginator.get_page(page_number)

        return render(request,'tasks-list.html',{'data':data,'conversation_data':conversation_data,'filter':filter})


@login_required(login_url='login')
def closed_task_list(request):
    if request.user.is_superuser:
        task_data = TaskManagement.objects.filter(status='close')
        filter = TaskFilter(request.GET, queryset=task_data)
        data = filter.qs

        task_conversation_data = []

        for data in data:
            convo_data = TaskConversation.objects.filter(task_id=data.id).last()
            if convo_data:
                message = convo_data.message_by.username
            else:
                message = 'no msg'
            task_conversation_data.append({
                'data': data,
                'message': message
            })
        paginator = Paginator(task_conversation_data, 20)  # Show 25 contacts per page.
        page_number = request.GET.get("page")
        conversation_data = paginator.get_page(page_number)

        return render(request, 'tasks-list.html', {'data': data,'conversation_data':conversation_data,'filter':filter})
    else:
        data = TaskManagement.objects.filter(task_assign_to=request.user,status='close')|TaskManagement.objects.filter(task_assign_from=request.user,status='close')
        filter = TaskFilter(request.GET, queryset=data)
        task_data = filter.qs

        task_conversation_data = []

        for data in task_data:
            convo_data = TaskConversation.objects.filter(task_id=data.id).last()
            if convo_data:
                message = convo_data.message_by.username
            else:
                message = 'no msg'
            task_conversation_data.append({
                'data': data,
                'message': message
            })
        paginator = Paginator(task_conversation_data, 20)  # Show 25 contacts per page.
        page_number = request.GET.get("page")
        conversation_data = paginator.get_page(page_number)

        return render(request,'tasks-list.html',{'data':task_data,'conversation_data':conversation_data,'filter':filter})



@login_required(login_url='login')
def delete_task_conversation(request,id):
    data = TaskConversation.objects.filter(id=id).first()
    if data.image:
        os.remove(data.image.path)
    data.delete()
    return redirect('task_list')



    