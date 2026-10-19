from django.contrib import admin

from leave.models import LeaveType,LeaveRequest,EmployeeLeave,LeaveHistory
from user_management.models import Department
from ticketing_support.models import TicketConversation, Tickets
admin.site.register(LeaveType)
admin.site.register(LeaveRequest)
admin.site.register(EmployeeLeave)
admin.site.register(LeaveHistory)
admin.site.register(Department)
admin.site.register(Tickets)
admin.site.register(TicketConversation)

