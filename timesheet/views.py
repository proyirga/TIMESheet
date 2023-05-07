from django.shortcuts import render, redirect, get_object_or_404

from . models import User, Project, Task, Entry, Timesheet
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView

@login_required
def dashboard(request):
    #get the current user
    user = request.user
    # get the current date
    today = datetime.date.today()
    # 

def send_timesheet_email(timesheet):
    # Import the EmailMessage class from django.core.mail
    from django.core.mail import EmailMessage
    # Get the manager email from settings.py
    from django.conf import settings
    managerEmail = settings.MANAGER_EMAIL
    # Create an email message with subject, body, from_email, and to_email
    subject = f'Timesheet submitted by {timesheet.user.username}'
    body = f'Please review and approve or reject this timesheet:\n\n{timesheet}\n\nYou can view it here: {timesheet.get_absolute_url()}'
    from_email = 'noreply@timesheet.com'
    to_email = [manager_email]
