from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
from rest_framework import generics, permissions
from .models import Todo
from .serializers import TodoSerializer
from account.permissions import IsOwnerOrAdmin

class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print("Incoming request data:", self.request.data)
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        print("POST request received:", request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TodoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

class TodoAdminListAPIView(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class TodoAdminBulkDeleteAPIView(generics.DestroyAPIView):
    queryset = Todo.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


