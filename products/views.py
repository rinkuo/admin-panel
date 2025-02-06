from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .forms import ProductForm
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.db.models import Q
from .models import Product, Category

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        search_query = self.request.GET.get('q', '')
        category_filter = self.request.GET.get('category', '')
        sort_option = self.request.GET.get('sort', '')

        # Filtering by search query
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )

        # Filtering by category
        if category_filter and category_filter != 'all':
            queryset = queryset.filter(category__id=category_filter)

        # Sorting options
        if sort_option == 'name':
            queryset = queryset.order_by('name')
        elif sort_option == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_option == 'price_desc':
            queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_sort'] = self.request.GET.get('sort', '')
        return context
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        # This method is called when the form is valid
        return super().form_valid(form)

    def form_invalid(self, form):
        # This method is called when the form is invalid
        print(form.errors)  # This will print errors to the server console
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'
    success_url = reverse_lazy('product_list')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/delete-confirm.html'
    success_url = reverse_lazy('products:product_list')