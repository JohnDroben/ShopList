from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Product, Category

class ProductListView(ListView):
    template_name = 'shop/product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                models.Q(name__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class CategoryView(ListView):
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['active_category'] = self.category
        return ctx

class ProductDetailView(DetailView):
    template_name = 'shop/product_detail.html'
    model = Product
    context_object_name = 'product'
    slug_field = 'slug'