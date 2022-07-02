from datetime import datetime
from tkinter import CASCADE
from django.db import models
from django.core.files import File
class Problem(models.Model):
    Problem_id = models.PositiveBigIntegerField(default = 0)
    Title = models.CharField(max_length = 50)
    Description = models.TextField()
    Input_Format = models.TextField()
    Output_Format = models.TextField()
    Constraint = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.Title

def get_upload_to(Problem,filename):
    return 'testfiles/%d/%s' %(Problem.Title,filename)

class TestCase(models.Model):
    Problem_Name = models.ForeignKey(Problem,on_delete = models.CASCADE)
    Input_File = models.FileField(upload_to = 'testfiles/input/')
    Output_file = models.FileField(upload_to = 'testfiles/output/')
    
    def __str__(self):
        return self.Problem.Title 

class Submission(models.Model):
      Problem = models.ForeignKey(Problem, on_delete = models.CASCADE)
      Submission_Time = models.DateTimeField(default = datetime.now)
      Language = models.CharField(max_length = 10)
      Code = models.FileField() 

      def __str__(self):
        return self.Problem.Title
