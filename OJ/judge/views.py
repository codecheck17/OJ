import os,subprocess
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Problem,TestCase,Submission
from django.core.files import File

def ProblemSet(request):
    problems = Problem.objects.all()
    context = {
        'problems' : problems
    }
    return render(request,'judge/ProblemSet.html',context)

def Description(request,Problem_id):
    CurrentProblem = get_object_or_404(Problem,pk = Problem_id)
    context = {
        'Problem_id' : Problem_id,
        'Title' : CurrentProblem.Title,
        'Description' : CurrentProblem.Description,
        'Input_Format' : CurrentProblem.Input_Format,
        'Output_Format' : CurrentProblem.Output_Format,
        'Constriants' : CurrentProblem.Constraint
    }
    return render(request,'judge/Description.html',context)

def NewSubmission(request,Problem_id):
    return render(request,'judge/NewSubmission.html')

def MySubmissions(request,Problem_id):
    return render(request,'judge/MySubmissions.html')

def Verdict(request,Problem_id):
    return render(request,'judge/Verdict.html')

