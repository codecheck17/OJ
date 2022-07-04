import os,subprocess
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .forms import CodeForm
from .models import Problem, Submission

def ProblemSet(request):
    problems = Problem.objects.all()
    context = {
        'problems' : problems
    }
    return render(request,'judge/ProblemSet.html',context)

def Description(request,Problem_id):
    CurrentProblem = get_object_or_404(Problem,pk = Problem_id)
    Sample_Input_Path = f'testfiles/{CurrentProblem.Title}/input/test_input_1.txt'
    Sample_Output_Path = f'testfiles/{CurrentProblem.Title}/output/test_output_1.txt'
    with open(Sample_Input_Path) as f:
          Sample_Input = f.read()
    with open(Sample_Output_Path) as f:
          Sample_Output = f.read()      
    
    context = {
        'Problem_id' : Problem_id,
        'Title' : CurrentProblem.Title,
        'Description' : CurrentProblem.Description,
        'Input_Format' : CurrentProblem.Input_Format,
        'Output_Format' : CurrentProblem.Output_Format,
        'Constriants' : CurrentProblem.Constraint,
        'Sample_Input': Sample_Input,
        'Sample_Output': Sample_Output,
    }
    return render(request,'judge/Description.html',context)

def findVerdict(Problem_id):
   return "Accepted"

def NewSubmission(request,Problem_id):
    thisProblem = get_object_or_404(Problem,pk = Problem_id)
    if request.method == 'POST': 
        thisSubmission = Submission(Problem = thisProblem)
        UploadedForm = CodeForm(request.POST,request.FILES,instance = thisSubmission)
        if UploadedForm.is_valid():
            thisSubmission.save()
            result = findVerdict(Problem_id)
            context = {
                'result': result,
            }
            return render(request,'judge/Verdict.html',context)
        else:
            return HttpResponse("somthing went wrong")       
    else:
        NewForm = CodeForm()
        context = {
            'Problem_Name': thisProblem.Title,
            'NewForm' : NewForm,
            'Problem_id' : Problem_id
        }
        return render(request,'judge/NewSubmission.html',context)

def MySubmissions(request,Problem_id):
    return render(request,'judge/MySubmissions.html')


