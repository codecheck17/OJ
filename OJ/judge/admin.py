from dataclasses import field
from django.contrib import admin
from .models import Problem,Submission,TestCase

class TestCaseInline(admin.StackedInline):
    model = TestCase
    extra = 1

class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 1

class ProblemAdmin(admin.ModelAdmin):
   list_display = ('Problem_id','Title')
   fieldsets = [
    (None,      {'fields':['Problem_id','Title','Description']}), 
    ('Input Details', {'fields':['Input_Format']}),
    ('Output Details', {'fields':['Output_Format']}),
    ('Constraint',{'fields':['Constraint']}),
   ]
   inlines = [TestCaseInline,SubmissionInline]

admin.site.register(Problem,ProblemAdmin)
admin.site.register(Submission)
admin.site.register(TestCase)



