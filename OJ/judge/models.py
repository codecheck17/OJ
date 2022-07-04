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

class TestCase(models.Model):
    
    def upload_file_name_input(self, filename):
        return f'testfiles/{self.Problem_Name.Title}/input/{filename}'
    
    def upload_file_name_output(self,filename):
        return f'testfiles/{self.Problem_Name.Title}/output/{filename}'
    
    Problem_Name = models.ForeignKey(Problem,on_delete = models.CASCADE)
    Input_File = models.FileField(upload_to = upload_file_name_input)
    Output_file = models.FileField(upload_to = upload_file_name_output)
    
    def __str__(self):
        return self.Problem_Name.Title 

class Submission(models.Model):
      
      Problem = models.ForeignKey(Problem, on_delete = models.CASCADE)
      def upload_code_name(self,filename):
        return f'codes/mycodes/{self.Problem.Title}/{filename}'
      
      Submission_Time = models.DateTimeField(default = datetime.now)
      Language = models.CharField(max_length = 10)
      Code = models.FileField(upload_to = upload_code_name) 

      def __str__(self):
        return self.Problem.Title


