from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def welcome(request):
    
    try:
        question = request.GET['question']
    except:
        question = ""
    
    return render_to_response("home.html", {}, context_instance=RequestContext(request))
