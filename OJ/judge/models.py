from datetime import datetime
from tkinter import CASCADE
from django.db import models


class Problem(models.Model):
    Problem_id = models.PositiveBigIntegerField(default = 0)
    Title = models.CharField(max_length = 50)
    Description = models.TextField()
    Input_Format = models.TextField()
    Output_Format = models.TextField()
    Constraint = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.Title

class TestCase(models.Model):
    Problem = models.ForeignKey(Problem,on_delete = models.CASCADE)
    Input_File = models.FileField()
    Output_file = models.FileField()
    
    def __str__(self):
        return self.Problem.Title 

class Submission(models.Model):
      Problem = models.ForeignKey(Problem, on_delete = models.CASCADE)
      Submission_Time = models.DateTimeField(default = datetime.now)
      Language = models.CharField(max_length = 10)
      Code = models.FileField() 

      def __str__(self):
        return self.Problem.Title
