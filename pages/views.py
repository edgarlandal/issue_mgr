from django.views.generic import TemplateView

# Create your views here.

class HomeListView(TemplateView):
    template_name = "pages/home.html"
