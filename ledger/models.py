from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Property(models.Model):
    """Model for real estate properties."""
    PROPERTY_TYPES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('mixed', 'Mixed Use'),
        ('land', 'Land'),
    ]
    
    name = models.CharField(max_length=200, help_text="Property name or identifier")
    address = models.TextField(help_text="Full property address")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='residential')
    acquisition_date = models.DateField(help_text="Date property was acquired")
    purchase_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Purchase price of the property"
    )
    current_value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        null=True, 
        blank=True,
        help_text="Current estimated value"
    )
    notes = models.TextField(blank=True, help_text="Additional notes about the property")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def total_income(self):
        """Calculate total income for this property."""
        return self.transactions.filter(
            transaction_type='income'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
    
    @property
    def total_expenses(self):
        """Calculate total expenses for this property."""
        return self.transactions.filter(
            transaction_type='expense'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
    
    @property
    def net_income(self):
        """Calculate net income for this property."""
        return self.total_income - self.total_expenses


class Transaction(models.Model):
    """Model for financial transactions related to properties."""
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    # Schedule E categories for income
    INCOME_CATEGORIES = [
        ('rent', 'Rent'),
        ('late_fees', 'Late Fees'),
        ('pet_fees', 'Pet Fees'),
        ('utilities_reimbursement', 'Utilities Reimbursement'),
        ('other_income', 'Other Income'),
    ]
    
    # Schedule E categories for expenses
    EXPENSE_CATEGORIES = [
        ('advertising', 'Advertising'),
        ('auto_travel', 'Auto and Travel'),
        ('cleaning_maintenance', 'Cleaning and Maintenance'),
        ('commissions', 'Commissions'),
        ('insurance', 'Insurance'),
        ('legal_professional', 'Legal and Professional Fees'),
        ('management_fees', 'Management Fees'),
        ('mortgage_interest', 'Mortgage Interest'),
        ('other_interest', 'Other Interest'),
        ('repairs', 'Repairs'),
        ('supplies', 'Supplies'),
        ('taxes', 'Taxes'),
        ('utilities', 'Utilities'),
        ('depreciation', 'Depreciation'),
        ('other_expenses', 'Other Expenses'),
    ]
    
    property = models.ForeignKey(
        Property, 
        on_delete=models.CASCADE, 
        related_name='transactions',
        help_text="Property this transaction is associated with"
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=50, help_text="Schedule E category")
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Transaction amount"
    )
    date = models.DateField(help_text="Date of transaction")
    description = models.CharField(max_length=200, help_text="Brief description of transaction")
    vendor = models.CharField(max_length=100, blank=True, help_text="Vendor or payee name")
    receipt_reference = models.CharField(max_length=100, blank=True, help_text="Receipt number or reference")
    notes = models.TextField(blank=True, help_text="Additional notes")
    is_recurring = models.BooleanField(default=False, help_text="Is this a recurring transaction?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.property.name} - {self.description} ({self.amount})"
    
    def save(self, *args, **kwargs):
        """Override save to set category choices based on transaction type."""
        if self.transaction_type == 'income':
            if self.category not in [cat[0] for cat in self.INCOME_CATEGORIES]:
                self.category = 'other_income'
        elif self.transaction_type == 'expense':
            if self.category not in [cat[0] for cat in self.EXPENSE_CATEGORIES]:
                self.category = 'other_expenses'
        super().save(*args, **kwargs)
