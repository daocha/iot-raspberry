from actions.functions import Action as act
from django.http import HttpResponse
from django.http import HttpResponseRedirect

# Add the two views we have been talking about  all this time :)
def index(request):
    return HttpResponseRedirect("/")

def check_iot_status(request):
    return HttpResponse(act.getThingState())


    