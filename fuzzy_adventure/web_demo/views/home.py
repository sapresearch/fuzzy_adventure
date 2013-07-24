from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from fuzzy_adventure.query_decomposition.nlidb.term_selectors.term_selector import TermSelector
import re

questionlist = [
 
        "Who is the most productive person on my team?",
        "What component contribute the most to my backlog?",
        "How many messages <(employee Name)> closed.",
        "How long does it take on average to close a ticket with priority <(priority level)>",
        "How long on average does it take <(person)> to close a ticket?",
        "How many messages <(employee Name)> touched.",
        "How long on average does it take to close a ticket?",
        "What is the average MPT when the messages get forwarded to our queue?",
        "How many escalated messages <(employee Name)> has worked on.",
        "Give me the list of the open messages for <(name of the topic)> topic.",
        "Give me the list of the messages without a processor.",
        #"When <(employee ID or employee Name)> started working on  <(name of a component)> component.",
    ]


def welcome(request):

    params = []
    try:
        question = request.GET['question']
    except:
        question = ""

        try:
            question_type = int(request.GET['question_type'])
        except:
            question_type =0

        if question_type:
            try:
                param1 = request.GET['param1']
                params.append(param1)
            except:
                param1 = ""

            try:
                param2 = request.GET['param2']
                params.append(param2)
            except:
                param2 = ""

    if question:
        from executable import FuzzyAdventure
        answers = FuzzyAdventure.web_demo(question.encode('ascii', 'ignore'))
    elif question_type:
        from executable import FuzzyAdventure
        question = questionlist[question_type-1]
        question = re.sub(r'<(.*?)>', param1, question) if param1 else question
        question = re.sub(r'<(.*?)>', param2, question) if param2 else  question
        sql_query = FuzzyAdventure.place_params(question_type, params)
        answers = TermSelector.filter_answers(TermSelector.crash_and_burn([sql_query]))
    else:
        answers = []

    context = {}
    context['question'] = question
    context['answer_ary'] = answers
    context['questionlist'] = questionlist

    return render_to_response("home.html", context, context_instance=RequestContext(request))

