import subprocess,re,os
import this

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import CodeForm
from .models import Problem, Submission, TestCase

Language_Choices = {
    '1':'C++',
    '2':'Java',
    '3':'Python',
}

Language_Container = {
    'C++':'gcc',
    'Java':'java',
    'Python':'python',
}

def findVerdict(Problem,Submission):
   CodePath = f'C:/OJ/OJ/{Submission.Code.url}'
   Verdict = "AC"
   Language = Submission.Language
   testcases = TestCase.objects.filter(Problem_Name = Problem)
   
   CompletedSubprocess = subprocess.run(f'docker run -d {Language_Container[Language]} tail -f /dev/null',capture_output = True)
   Container_id = CompletedSubprocess.stdout.decode()
   Container_id = Container_id[:-1]
   Container_file = CodePath.split('/')[-1]
   subprocess.run(f'docker cp {CodePath} {Container_id}:/{Container_file}')
   
   if Language == 'C++':
        subprocess.run(f'docker exec {Container_id} g++ {Container_file}') 
   elif Language == 'Java':
        Executable_name = os.path.splitext(Container_file)[0]
        subprocess.run(f'docker exec {Container_id} javac {Container_file}')   
   
   for testcase in testcases:
        
        inputFile = f'C:/OJ/OJ/{testcase.Input_File.url}'  
        actual_outputFile = f'C:/OJ/OJ/{testcase.Output_file.url}'   
        outputFile = f'C:/OJ/OJ/Output.txt'
       
        subprocess.run(f'docker cp {inputFile} {Container_id}:/input.txt')
        if Language == 'C++':
            subprocess.run(f'docker exec {Container_id} sh -c "./a.out < input.txt > output.txt"')
        elif Language == 'Java':
            subprocess.run(f'docker exec {Container_id} sh -c "java {Executable_name} < input.txt > output.txt"') 
        else :
            subprocess.run(f'docker exec {Container_id} sh -c "python {Container_file} < input.txt > output.txt"')     
         
        subprocess.run(f'docker cp {Container_id}:/output.txt {outputFile}')
        
        with open(outputFile, 'r') as file:
            data1 = file.read()
        
        with open(actual_outputFile, 'r') as file:
            data2 = file.read() 
        
        data1 = re.sub('[\n ]','',data1)
        data2 = re.sub('[\n ]','',data2) 
        if(data1!=data2):
            Verdict = "WA"
   
   subprocess.run(f'docker rm -f {Container_id}')
   with open(CodePath) as Codes:
      Code = Codes.read()
   
   return [Code,Verdict]


#=====================================================================================#


@login_required
def ProblemSet(request):
    username = request.user.username
    problems = Problem.objects.all()
    context = {
        'problems' : problems,
        'username': username
    }
    return render(request,'judge/ProblemSet.html',context)




#=====================================================================================#




@login_required
def Description(request,Problem_id):
    username = request.user.username
    CurrentProblem = get_object_or_404(Problem,pk = Problem_id)
    testcases = TestCase.objects.filter(Problem_Name = CurrentProblem)[:1]
    for testcase in testcases:
        Sample_Input_Path = f'C:/OJ/OJ/{testcase.Input_File.url}'
        Sample_Output_Path = f'C:/OJ/OJ/{testcase.Output_file.url}'
        
        with open(Sample_Input_Path) as ip,open(Sample_Output_Path) as op:
            Sample_Input = ip.read()
            Sample_Output = op.read()    
    
    context = {
        'username': username,
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


#===========================================================================================#


@login_required
def NewSubmission(request,Problem_id):
    username = request.user.username
    thisProblem = get_object_or_404(Problem,pk = Problem_id)
    if request.method == 'POST': 
        thisSubmission = Submission(Problem = thisProblem)
        UploadedForm = CodeForm(request.POST,request.FILES,instance = thisSubmission)
        if UploadedForm.is_valid():
            Language_Option = UploadedForm.cleaned_data['Language_Select']
            thisSubmission.Language = Language_Choices[Language_Option]
            thisSubmission.UserName = username
            thisSubmission.SubmissionId = Submission.objects.all().count()+1
            thisSubmission.save()
            Code = findVerdict(thisProblem,thisSubmission)
            thisSubmission.Result = Code[1]
            thisSubmission.save() 
            context = {
                'username' : username,
                'Code':  Code[0],
                'result': Code[1],
                'Language':thisSubmission.Language
            }
            return render(request,'judge/Verdict.html',context)
        else:
            return HttpResponse("somthing went wrong")       
    else:
        NewForm = CodeForm()
        context = {
            'username' : username,
            'Problem_Name': thisProblem.Title,
            'NewForm' : NewForm,
            'Problem_id' : Problem_id
        }
    
    return render(request,'judge/NewSubmission.html',context)





#=====================================================================================#

class TemplateSubmission():
    SubmissionId = None
    SubmissionTime = None
    problem = None
    folder = None
    user = None
    filename = None
    Result = None
    Language = None



@login_required
def MySubmissions(request,Problem_id):
    thisProblem = get_object_or_404(Problem,pk=Problem_id)
    username = request.user.username
    SubmissionList=Submission.objects.filter(Problem = thisProblem,UserName = username).order_by('-Submission_Time')[:5]
    TemplateSubmissionList = []
    for thisSubmission in SubmissionList:
        Template = TemplateSubmission()
        Template.Language = thisSubmission.Language
        Template.Result = thisSubmission.Result
        Template.SubmissionTime = thisSubmission.Submission_Time
        thisList = thisSubmission.Code.url.split('/')
      
        Template.folder = thisList[1]
        Template.problem = thisList[2]
        Template.user = thisList[3]
        Template.SubmissionId = thisList[4]
        Template.filename = thisList[5]

        TemplateSubmissionList.append(Template)
    
    context = {
        'SubmissionList': TemplateSubmissionList
    }
    return render(request,'judge/MySubmissions.html',context)

#======================================================================================#

@login_required
def SubmissionDetail(request,folder,problem,user,subid,filename):

    with open(f'C:/OJ/OJ/{folder}/{problem}/{user}/{subid}/{filename}') as Codes:
        Code = Codes.read()
    
    context = {
        'Code' : Code
    }
    return render(request,'judge/SubmissionDetail.html',context)