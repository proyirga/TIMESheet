from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

User = User

class Project(models.Model):
    projectId = models.CharField(max_length=100)
    projectName = models.CharField(max_length=200)
    projectDescription = models.TextField()
    projectStartDate = models.DateField()
    projectEndDate = models.DateField()
    users = ManyToManyField(User)

    def __str__(self):
        return self.projectName

class Task(models.Model):
    taskName = models.CharField(max_length=100)
    taskDescription = models.TextField()
    taskStartTime = modles.DateTimeField()
    taskEndTime = models.DateTimeField()
    taskStatus = modles.CharFiled(max_length=100, choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.taskName

class Entry(models.Model):
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    duration = models.DurationField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.task} - {self.date}'
class Timesheet(models.Model):
    date = models.DateField()
    weekStart = models.DateField()
    weekEnd = models.DateField
    user = models.ForeignKey(User, on_delete=CASCADE)
    project = models.ForeignKey(Project, on_delete=CASCADE)

    def __str__(self):
    return f'{self.user} - {self.weekStart} to {self.weekEnd}'
    
    def get_absolute_url(self):
    # Return the URL for the model object using the app_name and the url name
    return reverse('timesheet:detailTimesheet', args=[self.id])

@property
def status(self):
    # Return 'Approved' if the timesheet is approved or 'Rejected' if it is rejected or 'Pending' otherwise
    if self.approved:
        return 'Approved'
    elif self.rejected:
        return 'Rejected'
    else:
        return 'Pending'
