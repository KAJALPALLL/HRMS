# from django.shortcuts import render,redirect
#
# from . models import Leave,LeaveRequest
#
# from . forms import LeaveForm,LeaveRequestForm
#
#
# def add_leave_type(request):
#     if request.method == "POST":
#         form = LeaveForm(request.POST)
#         if form.is_valid:
#             form.save()
#             return redirect('leave_list')
#         else:
#             return redirect('add_leave_type')
#     else:
#         form = LeaveForm()
#         return render(request,'add-leave-type.html',{'form':form})
#
# def leave_list(request):
#     data = Leave.objects.all()
#     return render(request,'leave-list.html',{'data':data})
#
#
# def update_leave_type(request,id):
#     leave_data = Leave.objects.get(id=id)
#     if request.method == "POST":
#         form = LeaveForm(request.POST,instance=leave_data)
#         if form.is_valid:
#             form.save()
#             return redirect('leave_list')
#         else:
#             return render(redirect,'update_leave_type',id)
#     else:
#         form = LeaveForm(instance=leave_data)
#         return render(request,'update-leave-type.html',{'form':form})
#
# def delete_leave_type(request,id):
#     data = Leave.objects.filter(id=id)
#     data.delete()
#     return redirect('leave_list')
#
#
# def add_leave_request(request):
#     if request.method == "POST":
#         form = LeaveRequestForm(request.POST)
#         if form.is_valid:
#             form.save()
#             return redirect('leave_request_list')
#         else:
#             return redirect('add_leave_request')
#     else:
#         form = LeaveRequestForm()
#         return render(request,'add-leave-request.html',{'form':form})
#
# def leave_request_list(request):
#     data = LeaveRequest.objects.all()
#     return render(request,'leave-request-list.html',{'data':data})
#
# def update_leave_request(request,id):
#     leave_apply_data = LeaveRequest.objects.get(id=id)
#     if request.method == "POST":
#         form = LeaveRequestForm(request.POST,instance=leave_apply_data)
#         if form.is_valid:
#             form.save()
#             return redirect('leave_request_list')
#         else:
#             return redirect('update_leave_request',id)
#     else:
#         form = LeaveRequestForm(instance=leave_apply_data)
#         return render(request,'update-leave-request.html',{'form':form})
#
# def delete_leave_request(request,id):
#     data = LeaveRequest.objects.filter(id=id)
#     data.delete()
#     return redirect('leave_request_list')