from django.http import HttpResponse
from django.shortcuts import render_to_response
import os
import sys
sys.path.append(os.environ['FUZZY_ADVENTURE'])
import executable
import settings

def home(request):
	return render_to_response('search_form.html', {'STATIC_URL', settings.STATIC_URL})


def search(request):
    if 'q' in request.GET and request.GET['q'] is not u'':
        answer, lat_type = executable.to_sql(request.GET['q'])
    else:
        answer = 'You asked for nothing, and nothing you shall get.'
    return HttpResponse(answer)