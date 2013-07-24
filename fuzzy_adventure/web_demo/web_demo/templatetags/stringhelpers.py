from django import template
import re

register = template.Library()

@register.filter(name="empty")
def empty(question):
    return re.sub(r"<(.*?)>", "______", question);

@register.filter(name="repl")
def repl(question, count):
    return re.sub(r'<(.*?)>', r'<input type="text" class="input-large inputbox'+str(count)+'" placeholder="\1" >', question)


