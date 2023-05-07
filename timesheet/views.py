from django.shortcuts import render, redirect, get_object_or_404

from . models import User, Project, Task, Entry, Timesheet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView

@login_required
def dashboard(request):
    # Get the current user
    user = request.user
    # Get the current date
    today = datetime.date.today()
    # Get the start and end dates of the current week
    startDate = today - datetime.timedelta(days=today.weekday())
    endDate = startDate + datetime.timedelta(days=6)
    # Get the entries for the current week
    entries = Entry.objects.filter(user=user, dateRange=[startDate, endDate])
    # Calculate the total hours for the current week
    totalHours = datetime.timedelta()
    for entry in entries:
        totalHours += entry.duration
    # Check if the timesheet for the current week is submitted or not
    submitted = user.timesheets.filter(weekStart=startDate).exists()
    # Render the dashboard template with the following context data
    context = {
        'user': user,
        'entries': entries,
        'totalHours': totalHours,
        'submitted': submitted,
        'startDate': startDate,
        'endDate': endDate,
    }
    return render(request, 'timesheet/dashboard.html', context)

@login_required
def addEntry(request):
    # Get the current user
    user = request.user
    # Get the current date and time
    today = datetime.date.today()
    now = datetime.datetime.now().time()
    # If the request method is POST, process the form data
    if request.method == 'POST':
        # Get the form data from the request
        date = request.POST.get('date')
        startTime = request.POST.get('startTime')
        endTime = request.POST.get('endTime')
        taskId = request.POST.get('task')
        # Validate and convert the form data to Python objects
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            startTime = datetime.datetime.strptime(startTime, '%H:%M').time()
            endTime = datetime.datetime.strptime(endTime, '%H:%M').time()
            task = get_object_or_404(Task, id=taskId)
            duration = datetime.datetime.combine(date, endTime) - datetime.datetime.combine(date, startTime)
            if duration <= datetime.timedelta():
                raise ValueError('End time must be after start time')
        except ValueError as e:
            # If there is a validation error, return an error message
            return render(request, 'timesheet/addEntry.html', {'error': str(e)})
        # Create a new entry object with the form data
        entry = Entry(date=date, startTime=startTime, endTime=endTime, duration=duration, task=task, user=user)
        # Save the entry object to the database
        entry.save()
        # Redirect to the dashboard view with a success message 
        return redirect(‘timesheet:dashboard’)
    else:
        # Get the tasks that the user can work on 
        tasks = Task.objects.filter(users=user) 
        # Render the add entry template with the context data 
        context = { 
                'user': user,
                'tasks': tasks,
                'today': today,
                'now': now,
                }
        return render(request, ‘timesheet/addEntry.html’, context)

@login_required
def editEntry(request, entryId):
    # Get the current user
    user = request.user
    # Get the entry object or raise a 404 error if it does not exist
    entry = get_object_or_404(Entry, id=entryId)
    # Check if the entry belongs to the user or raise a 403 error if not
    if entry.user != user:
        return HttpResponseForbidden('You are not authorized to edit this entry')
    # If the request method is POST, process the form data
    if request.method == 'POST':
        # Get the form data from the request
        date = request.POST.get('date')
        startTime = request.POST.get('startTime')
        endTime = request.POST.get('endTime')
        taskId = request.POST.get('task')
        # Validate and convert the form data to Python objects
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            startTime = datetime.datetime.strptime(startTime, '%H:%M').time()
            endTime = datetime.datetime.strptime(endTime, '%H:%M').time()
            task = get_object_or_404(Task, id=taskId)
            duration = datetime.datetime.combine(date, endTime) - datetime.datetime.combine(date, startTime)
            if duration <= datetime.timedelta():
                raise ValueError('End time must be after start time')
        except ValueError as e:
            # If there is a validation error, return an error message
            return render(request, 'timesheet/editEntry.html', {'error': str(e), 'entry': entry})
        # Update the entry object with the form data
        entry.date = date
        entry.startTime = startTime
        entry.endTime = endTime
        entry.duration = duration
        entry.task = task
        # Save the entry object to the database
        entry.save()
        # Redirect to the dashboard view with a success message
        return redirect('timesheet:dashboard')
    # If the request method is GET, render the edit entry template with the existing data
    else:
        # Get the tasks that the user can work on
        tasks = Task.objects.filter(users=user)
        # Render the edit entry template with the context data
        context = {
            'user': user,
            'tasks': tasks,
            'entry': entry,
        }
        return render(request, 'timesheet/editEntry.html', context)

@login_required
def deleteEntry(request, entryId):
    # Get the current user
    user = request.user
    # Get the entry object or raise a 404 error if it does not exist
    entry = get_object_or_404(Entry, id=entryId)
    # Check if the entry belongs to the user or raise a 403 error if not
    if entry.user != user:
        return HttpResponseForbidden('You are not authorized to delete this entry')
    # If the request method is POST, delete the entry object from the database and redirect to the dashboard view with a success message
    if request.method == 'POST':
        entry.delete()
        return redirect('timesheet:dashboard')
    # If the request method is GET, render a confirmation page for deleting the entry
    else:
        return render(request, 'timesheet/deleteEntry.html', {'entry': entry})


@login_required
def submitTimesheet(request):
    # Get the current user
    user = request.user
    # Get the current date and time
    today = datetime.date.today()
    now = datetime.datetime.now().time()
    # Get the start and end dates of the current week
    startDate = today - datetime.timedelta(days=today.weekday()) endDate = startDate + datetime.timedelta(days=6)
    #Get the entries for the current week
    entries = Entry.objects.filter(user=user, date__range=[startDate, endDate])
    #Check if the timesheet for the current week is already submitted or not
    submitted = user.timesheets.filter(weekStart=startDate).exists()
    #If the timesheet is already submitted, redirect to the dashboard view with an error message
    if submitted: 
        return redirect('timesheet:dashboard')
    #If the request method is POST, create a new timesheet object with the entries and user data and save it to the database
    if request.method == 'POST': 
        timesheet = Timesheet(weekStart=startDate, weekEnd=endDate, user=user)
        timesheet.save()
        # Add the entries to the timesheet object 
        timesheet.entries.add(*entries) 
        # Send an email notification to the manager with the timesheet details
        sendTimesheetEmail(timesheet) 
        # Redirect to the dashboard view with a success message 
        return redirect('timesheet:dashboard')
    #If the request method is GET, render a confirmation page for submitting the timesheet
    else: 
        return render(request, 'timesheet/submitTimesheet.html', {'entries': entries})

@login_required
def viewTimesheets(request):
    # Get the current user
    user = request.user
    # Get all the timesheets submitted by the user
    timesheets = user.timesheets.all()
    # Render the view timesheets template with the context data
    context = {
        'user': user,
        'timesheets': timesheets,
    }
    return render(request, 'timesheet/viewTimesheets.html', context)


def sendTimesheetEmail(timesheet):
    # Import the EmailMessage class from django.core.mail
    from django.core.mail import EmailMessage
    # Get the manager email from settings.py
    from django.conf import settings
    managerEmail = settings.MANAGER_EMAIL
    # Create an email message with subject, body, from_email, and to_email
    subject = f'Timesheet submitted by {timesheet.user.username}'
    body = f'Please review and approve or reject this timesheet:\n\n{timesheet}\n\nYou can view it here: {timesheet.get_absolute_url()}'
    fromEmail = 'noreply@timesheet.com'
    toEmail = [managerEmail]
