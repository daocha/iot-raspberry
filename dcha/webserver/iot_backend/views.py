from actions.functions import Action as act
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView # Import TemplateView

# Add the two views we have been talking about  all this time :)
class HomePageView(TemplateView):
    template_name = "index.html"

def index(request):
    return HttpResponseRedirect("/")

def check_iot_status(request):
    return HttpResponse(act.getThingState())
    