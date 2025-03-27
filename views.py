from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Machine, Calibration
import json
from datetime import datetime


# Dashboard View with Calendar Filters
@login_required
def dashboard(request):
    machines = Machine.objects.all()
    statuses = ['Scheduled', 'Completed', 'Pending']

    # Get filter values from request
    machine_id = request.GET.get('machine')
    status = request.GET.get('status')
    selected_year = request.GET.get('year')
    selected_month = request.GET.get('month')

    # Convert month name to month number
    month_map = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }

    # Fetch calibrations based on filters
    calibrations = Calibration.objects.all()

    if machine_id:
        calibrations = calibrations.filter(machine_id=machine_id)
    if status:
        calibrations = calibrations.filter(status=status)
    if selected_year:
        calibrations = calibrations.filter(date__year=selected_year)
    if selected_month and selected_month in month_map:
        calibrations = calibrations.filter(date__month=month_map[selected_month])

    # Convert calibrations to JSON for FullCalendar
    events = [
        {
            'title': f'{calibration.machine.name} - {calibration.status}',
            'start': calibration.date.strftime('%Y-%m-%d') if calibration.date else '',
            'backgroundColor': '#0078D7' if calibration.status == 'Scheduled' else 
                              ('#28a745' if calibration.status == 'Completed' else '#dc3545'),
        }
        for calibration in calibrations
    ]

    return render(request, 'scheduler/dashboard.html', {
        'events': json.dumps(events),
        'machines': machines,
        'statuses': statuses,
        'years': range(datetime.now().year - 2, datetime.now().year + 3),
        'months': list(month_map.keys()),
    })



@login_required
def get_calendar_events(request):
    calibrations = Calibration.objects.all()

    events = [
        {
            "title": f"{calibration.machine.name} - {calibration.status}",
            "start": calibration.date.strftime('%Y-%m-%d'),
            "color": "#0078D7" if calibration.status == "Scheduled" else 
                     ("#28a745" if calibration.status == "Completed" else "#dc3545"),
        }
        for calibration in calibrations if calibration.date
    ]

    return JsonResponse(events, safe=False)



#  Machine Views
@login_required
def machine_list(request):
    return render(request, 'scheduler/machine_list.html', {'machines': Machine.objects.all()})


@login_required
def machine_detail(request, pk):
    return render(request, 'scheduler/machine_detail.html', {'machine': get_object_or_404(Machine, pk=pk)})


@login_required
def add_machine(request):
    if request.method == "POST":
        name = request.POST.get("name")
        type = request.POST.get("type")
        location = request.POST.get("location")

        if name and type and location:
            Machine.objects.create(name=name, type=type, location=location)
            return redirect('machine_list')

    return render(request, 'scheduler/add_machine.html')


@login_required
def edit_machine(request, pk):
    machine = get_object_or_404(Machine, pk=pk)

    if request.method == "POST":
        machine.name = request.POST.get("name")
        machine.type = request.POST.get("type")
        machine.location = request.POST.get("location")
        machine.save()
        return redirect('machine_list')

    return render(request, 'scheduler/edit_machine.html', {'machine': machine})


@login_required
def delete_machine(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    if request.method == "POST":
        machine.delete()
        return redirect('machine_list')

    return render(request, 'scheduler/delete_machine.html', {'machine': machine})


# Calibration Views
@login_required
def calibration_list(request):
    return render(request, 'scheduler/calibration_list.html', {'calibrations': Calibration.objects.all()})


@login_required
def schedule_calibration(request):
    if request.method == "POST":
        machine_id = request.POST.get("machine")
        date = request.POST.get("date")
        assigned_user_id = request.POST.get("assigned_user")

        if not date:
            messages.error(request, "Date is required!")
            return redirect('schedule_calibration')

        machine = get_object_or_404(Machine, pk=machine_id)
        assigned_user = User.objects.filter(pk=assigned_user_id).first()

        Calibration.objects.create(machine=machine, date=date, assigned_user=assigned_user)
        return redirect('calibration_list')

    return render(request, 'scheduler/schedule_calibration.html', {
        'machines': Machine.objects.all(),
        'users': User.objects.all(),
    })


@login_required
def update_calibration(request, pk):
    calibration = get_object_or_404(Calibration, pk=pk)

    if request.method == "POST":
        date = request.POST.get("date")
        status = request.POST.get("status")

        if not date:
            messages.error(request, "Date is required!")
            return redirect("update_calibration", pk=pk)

        calibration.date = date
        calibration.status = status
        calibration.save()
        return redirect("calibration_list")

    return render(request, "scheduler/update_calibration.html", {"calibration": calibration})


# User Authentication Views
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')

    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# Calendar View (For Full Calendar Display)
@login_required
def calendar_view(request):
    return render(request, 'scheduler/calendar.html')
