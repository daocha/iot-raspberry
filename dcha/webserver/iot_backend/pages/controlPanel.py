from django.views.generic import TemplateView # Import TemplateView
from actions.functions import Action as act

class ControlPanelView(TemplateView):
    template_name = "control_panel.html"
    
    def readStatus(self):
        return {"light":"0"}
