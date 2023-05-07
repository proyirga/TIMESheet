from django.urls import path
from . import views

appName = timesheet

urlpatterns = [
    # The path for the dashboard view
    path('dashboard/', views.dashboard, name='dashboard'),
    # The path for the add entry view
    path('addentry/', views.addEntry, name='addEntry'),
    # The path for the edit entry view with a parameter for the entry id
    path('editentry/<int:entryId>/', views.editEntry, name='editEntry'),
    # The path for the delete entry view with a parameter for the entry id
    path('deleteentry/<int:entryId>/', views.deleteEntry, name='deleteEntry'),
    # The path for the submit timesheet view
    path('submitTimesheet/', views.submitTimesheet, name='submitTimesheet'),
    # The path for the view timesheets view
    path('viewtimesheets/', views.viewTimesheets, name='viewTimesheets'),
]

