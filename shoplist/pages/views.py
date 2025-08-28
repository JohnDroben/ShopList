from django.views.generic import TemplateView
from shop.models import Product


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['products'] = Product.objects.all()[:12]
        return ctx


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class DeliveryView(TemplateView):
    template_name = 'pages/delivery.html'