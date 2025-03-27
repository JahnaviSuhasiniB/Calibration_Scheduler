from django.urls import path
from . import views

urlpatterns = [
    # Dashboard and Calendar
    path('', views.dashboard, name='dashboard'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('api/calendar/events/', views.get_calendar_events, name='get_calendar_events'),

    # Machine URLs
    path('machines/', views.machine_list, name='machine_list'),
    path('machines/<int:pk>/', views.machine_detail, name='machine_detail'),
    path('machines/add/', views.add_machine, name='add_machine'),
    path('machines/<int:pk>/edit/', views.edit_machine, name='edit_machine'),
    path('machines/<int:pk>/delete/', views.delete_machine, name='delete_machine'),

    # Calibration URLs
    path('calibrations/', views.calibration_list, name='calibration_list'),
    path('calibrations/schedule/', views.schedule_calibration, name='schedule_calibration'),
    path('calibrations/<int:pk>/update/', views.update_calibration, name='update_calibration'),

    # Authentication
    path('login/', views.login_view, name='login'),
]
