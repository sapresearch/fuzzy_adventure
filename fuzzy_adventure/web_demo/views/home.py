from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def welcome(request):
    try:
        question = request.GET['question']
    except:
        question = ""

    ''' Uncomment out this block when things work

        if question:
            from executable import FuzzyAdventure
            answers = [FuzzyAdventure.web_demo(question.encode('ascii', 'ignore'))]
        else:
            answers = []

    '''

    answers = ["a", "b", "c"]
    return render_to_response("home.html", {'question': question, 'answer_ary': answers}, context_instance=RequestContext(request))
