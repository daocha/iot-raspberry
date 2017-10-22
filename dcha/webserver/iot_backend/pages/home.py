from django.views.generic import TemplateView # Import TemplateView

class HomePageView(TemplateView):
    template_name = "index.html"