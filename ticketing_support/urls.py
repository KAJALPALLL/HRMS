from django.urls import path
from . import views

urlpatterns = [
    path('add-ticket',views.add_ticket,name='add_ticket'),
    path('ticket-list',views.ticket_list,name='ticket_list'),
    path('add-conversation',views.add_conversation,name='add_conversation'),
    path('conversation/<str:id>',views.conversation,name='conversation'),
    path('update-ticket-status/<str:id>',views.update_ticket_status,name='update_ticket_status'),
    path('client-tickets/<str:id>/<str:dep_id>',views.client_tickets,name='client_tickets'),

    path('update-ticket/<str:id>',views.update_ticket,name='update_ticket'),
    path('delete-ticket/<str:id>',views.delete_ticket,name='delete_ticket'),

    path('open-tickets',views.open_tickets,name='open_tickets'),
    path('closed-tickets',views.closed_tickets,name='closed_tickets'),

    path('delete-conversation/<str:id>/<str:t_id>',views.delete_conversation,name='delete_conversation'),

    path('pip-data',views.pip_data,name='pip_data'),




]