from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def about(request):
    return render_to_response("about.html", {}, context_instance=RequestContext(request))

def contact(request):
    return render_to_response("contact.html", {}, context_instance=RequestContext(request))
