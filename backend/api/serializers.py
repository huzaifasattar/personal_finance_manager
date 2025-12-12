from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Transaction, Budget, SavingsGoal


class UserSerializer(serializers.ModelSerializer):
    """User serializer for registration and profile"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""
    transaction_count = serializers.IntegerField(source='transactions.count', read_only=True)
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'type', 'color', 'icon', 'transaction_count', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer"""
    transaction_count = serializers.IntegerField(source='transactions.count', read_only=True)
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'transaction_count', 'created_at')
        read_only_fields = ('created_at',)


class TransactionSerializer(serializers.ModelSerializer):
    """Transaction serializer"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = (
            'id', 'amount', 'type', 'date', 'description', 
            'category', 'category_name', 'category_color',
            'tags', 'tags_list', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')
    
    def get_tags_list(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def validate(self, data):
        """Validate that category type matches transaction type"""
        category = data.get('category')
        transaction_type = data.get('type')
        
        if category and category.type != transaction_type:
            raise serializers.ValidationError(
                f"Category '{category.name}' is for {category.type} transactions, "
                f"but this is an {transaction_type} transaction."
            )
        return data


class BudgetSerializer(serializers.ModelSerializer):
    """Budget serializer"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    spent_amount = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = (
            'id', 'category', 'category_name', 'amount', 'period', 
            'year', 'month', 'spent_amount', 'remaining_amount', 
            'progress_percentage', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')
    
    def get_spent_amount(self, obj):
        """Calculate spent amount for this budget period"""
        from django.db.models import Sum
        from datetime import date
        
        transactions = Transaction.objects.filter(
            user=obj.user,
            category=obj.category,
            type='expense',
            date__year=obj.year
        )
        
        if obj.period == Budget.MONTHLY and obj.month:
            transactions = transactions.filter(date__month=obj.month)
        
        spent = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        return float(spent)
    
    def get_remaining_amount(self, obj):
        """Calculate remaining budget amount"""
        spent = self.get_spent_amount(obj)
        return float(obj.amount) - spent
    
    def get_progress_percentage(self, obj):
        """Calculate budget progress percentage"""
        spent = self.get_spent_amount(obj)
        if obj.amount == 0:
            return 0
        return min(100, (spent / obj.amount) * 100)


class SavingsGoalSerializer(serializers.ModelSerializer):
    """Savings goal serializer"""
    progress_percentage = serializers.FloatField(read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = SavingsGoal
        fields = (
            'id', 'name', 'target_amount', 'current_amount', 
            'deadline', 'progress_percentage', 'remaining_amount',
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')

