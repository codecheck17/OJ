from django.urls import path
from . import views
urlpatterns = [
    path('',views.ProblemSet,name = 'ProblemSet'),
    path('<int:Problem_id>/NewSubmission/',views.NewSubmission,name = 'NewSubmission'),
    path('<int:Problem_id>/MySubmissions/',views.MySubmissions,name = 'MySubmissions'),
    path('<int:Problem_id>/Description/',views.Description,name = 'Description'),
    path('<int:Problem_id>/SubmissionDetail/<CodePath>',views.SubmissionDetail,name = 'SubmissionDetail')
]
