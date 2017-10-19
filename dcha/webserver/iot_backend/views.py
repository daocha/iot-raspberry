from actions.functions import Action as act
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def check_iot_status(request):
    return HttpResponse(act.getThingState())
    