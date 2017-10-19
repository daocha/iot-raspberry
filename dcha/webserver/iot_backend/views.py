from actions.functions import Action as act
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def index(request):
    return HttpResponseRedirect("/")

def check_iot_status(request):
    return HttpResponse(act.getThingState())
    