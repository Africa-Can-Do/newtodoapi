from django.urls import path
from .views import TodoListCreateAPIView, TodoDetailAPIView, TodoAdminBulkDeleteAPIView, TodoAdminListAPIView

urlpatterns = [
    path('todos/', TodoListCreateAPIView.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', TodoDetailAPIView.as_view(), name='todo-detail'),
    path('admin/todos/', TodoAdminListAPIView.as_view(), name='todo-admin-list'),
    path('admin/todos/bulk-delete/', TodoAdminBulkDeleteAPIView.as_view(), name='todo-admin-bulk-delete'),
]
