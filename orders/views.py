from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from products.models import Product
from .forms import OrderForm, OrderItemForm
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Sum
from orders.models import Order, OrderItem
from collections import Counter

def dashboard_view(request):
    total_sales = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = Order.objects.count()
    new_customers = Order.objects.values('customer_name').distinct().count()
    sales_growth = 12
    orders_growth = 5
    customers_growth = 18

    recent_orders = Order.objects.order_by('-created_at')[:5]

    categories = Product.objects.values_list('category__name', flat=True)
    category_count = Counter(categories)

    category_labels = list(category_count.keys())
    category_counts = list(category_count.values())

    for order in recent_orders:
        order.status_color = order.get_status_color()

    return render(request, 'index.html', {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'new_customers': new_customers,
        'sales_growth': sales_growth,
        'orders_growth': orders_growth,
        'customers_growth': customers_growth,
        'recent_orders': recent_orders,
        'category_labels': category_labels,
        'category_counts': category_counts
    })



class OrderListView(ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = Order.objects.all()

        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(customer_name__icontains=search_query)

        queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for order in context['orders']:
            order.status_color = order.get_status_color()
        return context


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/form.html'
    success_url = reverse_lazy('orders:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        context['formset'] = OrderItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['order_id', 'order_date', 'status', 'customer_name', 'customer_phone', 'customer_email', 'customer_address', 'total_amount']
    template_name = 'orders/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        order_items = OrderItem.objects.filter(order=order)
        context['order_items'] = order_items
        OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        context['formset'] = OrderItemFormSet(instance=order)
        return context

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        formset = OrderItemFormSet(request.POST, instance=order)

        if 'add_item' in request.POST:
            if formset.is_valid():
                formset.save()
                return redirect('orders:order_update', pk=order.pk)

        elif 'save_order' in request.POST:
            form = self.get_form()
            if form.is_valid() and formset.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
                return redirect(self.get_success_url())

        context = self.get_context_data(**kwargs)
        context['formset'] = formset
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.pk})


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/detail.html'
    context_object_name = 'order'


class OrderDeleteView(DeleteView):
    model = OrderItem
    template_name = 'orders/delete.html'
    success_url = reverse_lazy('orders:order_list')


