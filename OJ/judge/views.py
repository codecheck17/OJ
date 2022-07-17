import subprocess,re,os

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from OJ.settings import BASE_DIR

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
   CodePath = f'{BASE_DIR}/{Submission.Code.url}'
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
        
        inputFile = f'{BASE_DIR}/{testcase.Input_File.url}'  
        actual_outputFile = f'{BASE_DIR}/{testcase.Output_file.url}'   
        outputFile = f'{BASE_DIR}/Output.txt'
       
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
   os.remove(outputFile)
   with open(CodePath) as Codes:
      Code = Codes.read()
   
   return [Code,Verdict]


#=====================================================================================#
@login_required
def SubmissionDetail(request,SubId,Problem_id):
    SubmissionList = Submission.objects.filter(SubmissionId = SubId)
    for aSubmission in SubmissionList:
        CodePath = f'{BASE_DIR}/{aSubmission.Code.url}'
        Problem_Name = aSubmission.Problem.Title
        Submission_time = aSubmission.Submission_Time
        Language = aSubmission.Language
        Result = aSubmission.Result
        with open(CodePath) as file:
            Codes = file.read()
        
    context = {
        'Problem_id': Problem_id,
        'Problem_Name': Problem_Name,
        'Submission_time':Submission_time,
        'Language': Language,
        'Result': Result,
        'username': request.user.username,
        'Code' : Codes
    }
    return render(request,'judge/SubmissionDetail.html',context)

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
        Sample_Input_Path = f'{BASE_DIR}/{testcase.Input_File.url}'
        Sample_Output_Path = f'{BASE_DIR}/{testcase.Output_file.url}'
        
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
            thisSubmission.Code = UploadedForm.cleaned_data['Code']
            thisSubmission.Language = Language_Choices[Language_Option]
            thisSubmission.UserName = username
            thisSubmission.SubmissionId = Submission.objects.all().count()+1
            thisSubmission.save()
            Code = findVerdict(thisProblem,thisSubmission)
            thisSubmission.Result = Code[1]
            thisSubmission.save() 
            context = {
                'username' : username,
                'Problem_id': Problem_id,
                'Problem_Name':thisProblem.Title,
                'Submission_time':thisSubmission.Submission_Time,
                'Language':thisSubmission.Language,
                'Code':  Code[0],
                'Result': Code[1]
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


@login_required
def MySubmissions(request,Problem_id):
    thisProblem = get_object_or_404(Problem,pk=Problem_id)
    username = request.user.username
    SubmissionList=Submission.objects.filter(Problem = thisProblem,UserName = username).order_by('-Submission_Time')
    context = {
        'username':username,
        'Problem_id':Problem_id,
        'SubmissionList': SubmissionList
    }
    return render(request,'judge/MySubmissions.html',context)

#======================================================================================#
