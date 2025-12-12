from django.shortcuts import render, redirect
from .models import MilkUser
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum
from .models import DailyRecord
from datetime import date
from django.utils import timezone
from django.db.models import Q, Sum


def index(request):
    return render(request, 'index.html')

def add_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        quality = request.POST.get('quality')
        rate = request.POST.get('rate')
        total_amount = request.POST.get('total_amount')
        shift = request.POST.get('shift')

        # Optional: prevent duplicates
        if MilkUser.objects.filter(name=name, mobile=mobile).exists():
            return render(request, 'adduser.html', {'error': 'User already exists.'})

        # Save to DB
        MilkUser.objects.create(
            name=name,
            mobile=mobile,
            address=address,
            quality=quality,
            rate=rate,
            total_amount=total_amount,
            shift=shift
        )
        return redirect('index')

    return render(request, 'adduser.html')


def user_list(request):
    shift = request.GET.get('shift')
    if shift:
        users = MilkUser.objects.filter(shift=shift)
    else:
        users = MilkUser.objects.all()
    return render(request, 'userdetail.html', {'users': users})


def user_detail(request, user_id):
    try:
        user = MilkUser.objects.get(id=user_id)
        return render(request, 'userdetail.html', {'users': [user]})
    except MilkUser.DoesNotExist:
        return render(request, '404.html', status=404)
    


def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(MilkUser, id=user_id)
        user.delete()
    return redirect('user_list')  # This should match the name of your user list view




def add_daily_amount(request, user_id):
    user = get_object_or_404(MilkUser, id=user_id)
    
    if request.method == 'POST':
        milk_quantity = float(request.POST.get('milk_quantity'))
        status = request.POST.get('status')
        entry_date = request.POST.get('date')

        # Auto-calculate amount
        amount = milk_quantity * float(user.rate)

        # Save record
        DailyRecord.objects.create(
            user=user,
            date=entry_date,
            milk_quantity=milk_quantity,
            amount=amount,
            status=status
        )
        return redirect('user_detail', user_id=user.id)

    context = {
        'user': user,
        'default_date': date.today().strftime('%Y-%m-%d')
    }
    return render(request, 'add_daily_amount.html', context)

def user_summary(request, user_id):
    user = get_object_or_404(MilkUser, id=user_id)
    records = DailyRecord.objects.filter(user=user).order_by('-date')

    total_amount = records.aggregate(total=Sum('amount'))['total'] or 0
    total_paid = records.filter(status='paid').aggregate(paid=Sum('amount'))['paid'] or 0
    pending_amount = total_amount - total_paid

    context = {
        'user': user,
        'records': records,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'pending_amount': pending_amount,
    }
    return render(request, 'user_summary.html', context)

def update_status(request, record_id):
    if request.method == 'POST':
        record = get_object_or_404(DailyRecord, id=record_id)
        new_status = request.POST.get('status')
        if new_status in ['paid', 'pending', 'unpaid']:
            record.status = new_status
            record.save()
    return redirect('user_summary', user_id=record.user.id)

def dashboard_view(request):
    total_users = MilkUser.objects.count()
    active_customers = MilkUser.objects.filter(shift__in=['morning', 'evening']).count()

    # ✅ First compute revenue and received
    total_revenue = DailyRecord.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    received_amount = DailyRecord.objects.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_amount = total_revenue - received_amount  # ✅ Safe to compute now

    # ✅ Inactive customers
    inactive_customers = MilkUser.objects.filter(Q(shift__isnull=True) | Q(shift='')).count()

    recent_orders = DailyRecord.objects.select_related('user').order_by('-date')[:5]
    all_users = MilkUser.objects.all()

    # Handle user filter dropdown
    selected_user_id = request.GET.get('user_id')
    selected_user_records = []
    if selected_user_id:
        selected_user_records = DailyRecord.objects.filter(user_id=selected_user_id).order_by('-date')

    context = {
        'total_orders': total_users,
        'total_revenue': total_revenue,
        'received_amount': received_amount,
        'pending_amount': pending_amount,
        'active_customers': active_customers,
        'inactive_customers': inactive_customers,  # ✅ Add to template
        'recent_orders': recent_orders,
        'inventory': {
            'Buffalo Milk': 150,
            'Cow Milk': 120,
            'Toned Milk': 80,
        },
        'all_users': all_users,
        'selected_user_records': selected_user_records,
        'selected_user_id': selected_user_id,
    }

    return render(request, 'dashboard.html', context)


def all_orders_view(request):
    all_orders = DailyRecord.objects.select_related('user').order_by('-date')
    return render(request, 'all_orders.html', {'all_orders': all_orders})