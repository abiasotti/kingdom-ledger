from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import Property, Transaction


def dashboard(request):
    """Dashboard view showing overview of all properties and transactions."""
    properties = Property.objects.all()
    transactions = Transaction.objects.all()
    
    # Calculate totals
    total_properties = properties.count()
    total_income = transactions.filter(transaction_type='income').aggregate(
        total=Sum('amount')
    )['total'] or 0
    total_expenses = transactions.filter(transaction_type='expense').aggregate(
        total=Sum('amount')
    )['total'] or 0
    net_income = total_income - total_expenses
    
    context = {
        'total_properties': total_properties,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': net_income,
        'properties': properties,  # Add properties to context
    }
    
    return render(request, 'ledger/dashboard.html', context)


def property_list(request):
    """List all properties."""
    properties = Property.objects.all()
    return render(request, 'ledger/property_list.html', {'properties': properties})


def property_add(request):
    """Add a new property."""
    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        address = request.POST.get('address')
        property_type = request.POST.get('property_type')
        acquisition_date = request.POST.get('acquisition_date')
        purchase_price = request.POST.get('purchase_price')
        current_value = request.POST.get('current_value')
        notes = request.POST.get('notes')
        
        # Create new property
        property_obj = Property.objects.create(
            name=name,
            address=address,
            property_type=property_type,
            acquisition_date=acquisition_date,
            purchase_price=purchase_price,
            current_value=current_value if current_value else None,
            notes=notes
        )
        
        # Redirect to property list
        return redirect('ledger:property_list')
    
    # GET request - show the form
    return render(request, 'ledger/property_form.html')


def property_detail(request, pk):
    """Show property details."""
    property_obj = get_object_or_404(Property, pk=pk)
    transactions = property_obj.transactions.all().order_by('-date')
    
    context = {
        'property': property_obj,
        'transactions': transactions,
    }
    return render(request, 'ledger/property_detail.html', context)


def property_edit(request, pk):
    """Edit an existing property."""
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        # Process form data
        property_obj.name = request.POST.get('name')
        property_obj.address = request.POST.get('address')
        property_obj.property_type = request.POST.get('property_type')
        property_obj.acquisition_date = request.POST.get('acquisition_date')
        property_obj.purchase_price = request.POST.get('purchase_price')
        current_value = request.POST.get('current_value')
        property_obj.current_value = current_value if current_value else None
        property_obj.notes = request.POST.get('notes')
        
        property_obj.save()
        
        # Redirect to property list
        return redirect('ledger:property_list')
    
    # GET request - show the form with existing data
    context = {
        'property': property_obj,
        'is_edit': True
    }
    return render(request, 'ledger/property_form.html', context)


def property_delete(request, pk):
    """Delete a property."""
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        # Delete the property
        property_obj.delete()
        return redirect('ledger:property_list')
    
    # GET request - show confirmation page
    return render(request, 'ledger/property_delete.html', {'property': property_obj})


def transaction_list(request):
    """List all transactions."""
    transactions = Transaction.objects.all().select_related('property')
    return render(request, 'ledger/transaction_list.html', {'transactions': transactions})


def transaction_add(request):
    """Add a new transaction."""
    properties = Property.objects.all()
    
    if request.method == 'POST':
        # Process form data
        property_id = request.POST.get('property')
        transaction_type = request.POST.get('transaction_type')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')
        vendor = request.POST.get('vendor')
        category = request.POST.get('category')
        notes = request.POST.get('notes')
        
        # Get the property object
        property_obj = Property.objects.get(id=property_id)
        
        # Create new transaction
        transaction = Transaction.objects.create(
            property=property_obj,
            transaction_type=transaction_type,
            amount=amount,
            date=date,
            description=description,
            vendor=vendor,
            category=category,
            notes=notes
        )
        
        # Redirect to transaction list
        return redirect('ledger:transaction_list')
    
    # GET request - show the form
    context = {
        'properties': properties,
    }
    return render(request, 'ledger/transaction_form.html', context)


def transaction_detail(request, pk):
    """Show transaction details."""
    return render(request, 'ledger/transaction_detail.html')


def transaction_edit(request, pk):
    """Edit an existing transaction."""
    return render(request, 'ledger/transaction_form.html')
