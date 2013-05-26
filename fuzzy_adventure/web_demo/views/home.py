from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from fuzzy_adventure import to_sql


def welcome(request):
    
    try:
        question = request.GET['question']
    except:
        question = ""

    answers = fuzzy_adventure.executable.to_sql(question)
 
    return render_to_response("home.html", {'question': question, 'answer_ary': answers}, context_instance=RequestContext(request))
