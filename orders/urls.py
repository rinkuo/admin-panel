from django.urls import path
from .views import OrderListView, OrderCreateView, OrderUpdateView, dashboard_view, OrderDetailView, OrderDeleteView

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('home/', dashboard_view, name='index'),
    path('new/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/edit/', OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete')
]