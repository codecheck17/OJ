import subprocess,os,re
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import CodeForm
from .models import Problem, Submission

Language_Choices = {
    '1':'C++',
    '2':'Java',
    '3':'Python',
    '4':'JavaScript',
    '5':'Haskell',
}

#=====================================================================================#



def ProblemSet(request):
    problems = Problem.objects.all()
    context = {
        'problems' : problems
    }
    return render(request,'judge/ProblemSet.html',context)




#=====================================================================================#





def Description(request,Problem_id):
    CurrentProblem = get_object_or_404(Problem,pk = Problem_id)
    FolderName = re.sub('[;:,. -+]','_',CurrentProblem.Title)
    Sample_Input_Path = f'testfiles/{FolderName}/input/test_input_1.txt'
    Sample_Output_Path = f'testfiles/{FolderName}/output/test_output_1.txt'
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


#===========================================================================================#


def findVerdict(Problem,Submission):
   filename = str(Submission.Submission_Time)
   filename = re.sub('[;:,. -+]', '_',filename)
   filename = filename+'.cpp'
   FolderName = re.sub('[;:,. -+]','_',Problem.Title)
   CodePath = 'codes/mycodes/'+ FolderName + '/' + filename
   Verdict = "AC"
   mydir = os.listdir('testfiles/'+ FolderName + '/input/')
   Count = len(mydir)
   for i in range(1,Count+1):
        
        inputFile = 'testfiles/'+ FolderName + '/input/test_input_' + str(i) + '.txt'  
        actual_outputFile = 'testfiles/'+ FolderName + '/output/test_output_' + str(i) + '.txt'  
        outputFile = 'C:/OJ/OJ/Output.txt'

        subprocess.run(['g++',CodePath,'-o','Output'])
        subprocess.call('Output <'+inputFile+'> C:/OJ/OJ/Output.txt',shell=True)
        
        with open(outputFile, 'r') as file:
            data1 = file.read()
        
        with open(actual_outputFile, 'r') as file:
            data2 = file.read() 
        
        data1 = re.sub('[\n ]','',data1)
        data2 = re.sub('[\n ]','',data2) 
        if(data1!=data2):
            Verdict = "WA"
   
   Code = []
   with open(CodePath) as Codes:
      for line in Codes:
        Code.append(line)
   
   Code.append(Verdict)
   return Code





#=====================================================================================#





def NewSubmission(request,Problem_id):
    thisProblem = get_object_or_404(Problem,pk = Problem_id)
    if request.method == 'POST': 
        thisSubmission = Submission(Problem = thisProblem)
        UploadedForm = CodeForm(request.POST,request.FILES,instance = thisSubmission)
        if UploadedForm.is_valid():
            Language_Option = request.POST['Language_Select']
            thisSubmission.Language=Language_Choices[Language_Option]
            thisSubmission.save()
            result = findVerdict(thisProblem,thisSubmission)
            thisSubmission.Result = result[-1]
            thisSubmission.save() 
            context = {
                'result': result,
                'Language':thisSubmission.Language
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





#=====================================================================================#





def MySubmissions(request,Problem_id):
    thisProblem = get_object_or_404(Problem,pk=Problem_id)
    SubmissionList=Submission.objects.filter(Problem = thisProblem).order_by('-Submission_Time')[:5]
    context = {
        'SubmissionList': SubmissionList
    }
    return render(request,'judge/MySubmissions.html',context)

#======================================================================================#

def SubmissionDetail(request,CodePath):
    return HttpResponse(str(CodePath))