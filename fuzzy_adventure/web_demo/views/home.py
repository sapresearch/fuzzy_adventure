from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
#from executable import FuzzyAdventure

def welcome(request):

    
    try:
        question = request.GET['question']
    except:
        question = ""

    if question:
        from executable import FuzzyAdventure
        answers = FuzzyAdventure.to_sql(question)
    else:
        answers = ""
 
    return render_to_response("home.html", {'question': question, 'answer_ary': answers}, context_instance=RequestContext(request))
