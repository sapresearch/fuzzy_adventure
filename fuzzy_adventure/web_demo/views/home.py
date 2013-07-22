from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import re

questionlist = [
        "How many messages <(employee ID or employee Name)> closed.",
        "How many messages <(employee ID or employee Name)> touched.",
        "How long a message stays in the SAP side?",
        "How many escalated messages <(employee ID or employee Name)> has worked on.",
        "What is the average MPT when the messages get forwarded to our queue?",
        "What is the average MPT when the messages get forwarded to our queue?",
        "When <(employee ID or employee Name)> started working on  <(name of a component)> component.",
        "Give me the list of the open messages for <(name of the topic)> topic.",
        "Give me the list of the messages without a processor.",
        "Give me the list of all the messages with <(name of the flag)> flag.",
        "Who is the most productive person on my team?",
        "What component contribute the most to my backlog?",
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
                params.add(param1)
            except:
                param1 = ""
            try:
                param2 = request.GET['param2']
                params.add(param2)
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
        answers = FuzzyAdventure.place_params(question_type, params)
    else:
        answers = []

    context = {}
    context['question'] = question
    context['answer_ary'] = answers
    context['questionlist'] = questionlist

    return render_to_response("home.html", context, context_instance=RequestContext(request))

