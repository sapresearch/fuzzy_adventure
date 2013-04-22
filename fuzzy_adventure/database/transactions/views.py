from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
import os
import sys
sys.path.append(os.environ['FUZZY_ADVENTURE'])
from fuzzy_adventure import executable
from fuzzy_adventure.database import settings

def home(request):
	t = loader.get_template('search_form.html')
	c = Context({'STATIC_URL', '/home/I834397/Git/fuzzy_adventure/database/transactions'})
	return HttpResponse(t.render(c))
	#return render_to_response('search_form.html', {' STATIC_URL ', settings.STATIC_URL})


def search(request):
    if 'q' in request.GET and request.GET['q'] is not u'':
        answer, lat_type = executable.to_sql(request.GET['q'])
    else:
        answer = 'You asked for nothing, and nothing you shall get.'
    return HttpResponse(answer)