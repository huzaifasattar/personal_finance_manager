from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Transaction categories (Income or Expense)"""
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    color = models.CharField(max_length=7, default='#1976d2', help_text='Hex color code')
    icon = models.CharField(max_length=50, blank=True, help_text='Icon name or identifier')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['name', 'user', 'type']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Tag(models.Model):
    """Tags for transactions"""
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['name', 'user']
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Income and Expense transactions"""
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]
    
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='transactions'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['-date', 'user']),
            models.Index(fields=['type', 'user']),
        ]
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} - {self.date}"


class Budget(models.Model):
    """Monthly or periodic budgets for categories"""
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
    PERIOD_CHOICES = [
        (MONTHLY, 'Monthly'),
        (YEARLY, 'Yearly'),
    ]
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='budgets',
        limit_choices_to={'type': 'expense'}
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default=MONTHLY)
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True, help_text='Required for monthly budgets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['category', 'user', 'year', 'month', 'period']
        ordering = ['-year', '-month']
    
    def __str__(self):
        period_str = f"{self.year}"
        if self.period == self.MONTHLY and self.month:
            period_str = f"{self.year}-{self.month:02d}"
        return f"Budget: {self.category.name} - {period_str}"


class SavingsGoal(models.Model):
    """Savings goals with target amounts"""
    name = models.CharField(max_length=200)
    target_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    current_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    deadline = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_goals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_amount == 0:
            return 0
        return min(100, (self.current_amount / self.target_amount) * 100)
    
    @property
    def remaining_amount(self):
        """Calculate remaining amount to reach goal"""
        return max(Decimal('0.00'), self.target_amount - self.current_amount)
    
    def __str__(self):
        return f"{self.name} - {self.current_amount}/{self.target_amount}"
