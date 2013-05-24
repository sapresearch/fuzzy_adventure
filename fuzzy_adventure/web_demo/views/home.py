from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def welcome(request, template = "home.html"):
    return render_to_response(template, {}, context_instance=RequestContext(request))
