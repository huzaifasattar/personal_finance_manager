from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Category, Tag, Transaction, Budget, SavingsGoal
from .serializers import (
    CategorySerializer, TagSerializer, TransactionSerializer,
    BudgetSerializer, SavingsGoalSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing categories"""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Return categories for the current user"""
        queryset = Category.objects.filter(user=self.request.user)
        
        # Filter by type if provided
        category_type = self.request.query_params.get('type', None)
        if category_type:
            queryset = queryset.filter(type=category_type)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the user when creating a category"""
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet for managing tags"""
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Return tags for the current user"""
        return Tag.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user when creating a tag"""
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing transactions"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        """Return transactions for the current user"""
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filter by type if provided
        transaction_type = self.request.query_params.get('type', None)
        if transaction_type:
            queryset = queryset.filter(type=transaction_type)
        
        # Filter by category if provided
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.select_related('category').prefetch_related('tags')
    
    def perform_create(self, serializer):
        """Set the user when creating a transaction"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get transaction summary (total income, total expenses, balance)"""
        user = request.user
        
        # Get date range from query params or use current month
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        if not start_date or not end_date:
            today = timezone.now().date()
            start_date = today.replace(day=1)
            # Get last day of month
            if today.month == 12:
                end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        transactions = Transaction.objects.filter(
            user=user,
            date__range=[start_date, end_date]
        )
        
        total_income = transactions.filter(type='income').aggregate(
            Sum('amount')
        )['amount__sum'] or 0
        
        total_expenses = transactions.filter(type='expense').aggregate(
            Sum('amount')
        )['amount__sum'] or 0
        
        balance = total_income - total_expenses
        
        return Response({
            'start_date': start_date,
            'end_date': end_date,
            'total_income': float(total_income),
            'total_expenses': float(total_expenses),
            'balance': float(balance),
            'transaction_count': transactions.count()
        })


class BudgetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing budgets"""
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['year', 'month', 'created_at']
    ordering = ['-year', '-month']
    
    def get_queryset(self):
        """Return budgets for the current user"""
        queryset = Budget.objects.filter(user=self.request.user)
        
        # Filter by year if provided
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(year=year)
        
        # Filter by period if provided
        period = self.request.query_params.get('period', None)
        if period:
            queryset = queryset.filter(period=period)
        
        return queryset.select_related('category')
    
    def perform_create(self, serializer):
        """Set the user when creating a budget"""
        serializer.save(user=self.request.user)


class SavingsGoalViewSet(viewsets.ModelViewSet):
    """ViewSet for managing savings goals"""
    serializer_class = SavingsGoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'deadline', 'target_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return savings goals for the current user"""
        return SavingsGoal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user when creating a savings goal"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_amount(self, request, pk=None):
        """Add amount to savings goal"""
        goal = self.get_object()
        amount = request.data.get('amount', 0)
        
        try:
            amount = float(amount)
            if amount <= 0:
                return Response(
                    {'error': 'Amount must be greater than 0'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            goal.current_amount += amount
            goal.save()
            
            serializer = self.get_serializer(goal)
            return Response(serializer.data)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid amount'},
                status=status.HTTP_400_BAD_REQUEST
            )
