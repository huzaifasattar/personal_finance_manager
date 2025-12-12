from django.contrib import admin
from .models import Category, Tag, Transaction, Budget, SavingsGoal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user', 'color', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'type', 'date', 'category', 'user', 'created_at')
    list_filter = ('type', 'date', 'category', 'created_at')
    search_fields = ('description', 'user__username', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'period', 'year', 'month', 'user', 'created_at')
    list_filter = ('period', 'year', 'month', 'created_at')
    search_fields = ('category__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_amount', 'current_amount', 'deadline', 'user', 'created_at')
    list_filter = ('deadline', 'created_at')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'progress_percentage', 'remaining_amount')
