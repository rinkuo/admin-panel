from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import CategoryForm
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.db.models import Count
from .models import Category

class CategoryListView(ListView):
    model = Category
    template_name = 'categories/list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count('product'))


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/form.html'
    success_url = reverse_lazy('categories:category_list')

    def form_valid(self, form):
        print("Form is valid, saving category...")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/form.html'
    success_url = reverse_lazy('categories:category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'categories/delete-confirm.html'
    success_url = reverse_lazy('categories:category_list')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/detail.html'
    context_object_name = 'category'
