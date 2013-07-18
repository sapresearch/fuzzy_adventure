def about(request):
    return render_to_response("about.html", {}, context_instance=RequestContext(request))

def contact(request):
    return render_to_response("contact.html", {}, context_instance=RequestContext(request))
