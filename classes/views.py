from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import FitnessClass, ClassCategory, ClassSchedule
from .forms import ScheduleCreationForm, BulkScheduleCreationForm, FitnessClassForm


def all_classes(request):
    """View to show all fitness classes, with filtering by category"""
    classes = FitnessClass.objects.all()
    categories = ClassCategory.objects.all()
    current_category = None
    search_query = None
    sort = None
    direction = None
    
    if request.GET:
        if 'category' in request.GET:
            category_name = request.GET['category']
            classes = classes.filter(category__name=category_name)
            current_category = ClassCategory.objects.get(name=category_name)
        
        if 'q' in request.GET:
            search_query = request.GET['q']
            if search_query:
                queries = Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(instructor__icontains=search_query)
                classes = classes.filter(queries)
        
        if 'sort' in request.GET:
            sort = request.GET['sort']
            sortkey = sort
            
            if sortkey == 'name':
                sortkey = 'name'
            
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            
            classes = classes.order_by(sortkey)
    
    current_sorting = f'{sort}_{direction}'
    
    context = {
        'classes': classes,
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query,
        'current_sorting': current_sorting,
    }
    
    return render(request, 'classes/all_classes.html', context)


def class_detail(request, class_id):
    """View to show individual class details"""
    fitness_class = get_object_or_404(FitnessClass, pk=class_id)
    
    context = {
        'fitness_class': fitness_class,
    }
    
    return render(request, 'classes/class_detail.html', context)


def class_schedule_list(request):
    """View to display class schedules, filtered by date (future only)"""
    # Get current datetime
    now = timezone.now()
    today = now.date()
    
    # Calculate default date range (current week: Monday to Sunday)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get date range from request or use defaults
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = start_of_week
    else:
        start_date = today  # Show from today onwards by default
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            end_date = None
    
    # Filter schedules: future only and active
    schedules = ClassSchedule.objects.filter(
        date__gte=start_date,
        is_active=True
    ).select_related('fitness_class', 'fitness_class__category')
    
    # Apply end date filter if specified
    if end_date:
        schedules = schedules.filter(date__lte=end_date)
    
    # Filter by class if specified
    class_id = request.GET.get('class_id')
    if class_id:
        schedules = schedules.filter(fitness_class_id=class_id)
    
    # Calculate quick date ranges
    next_week_start = start_of_week + timedelta(days=7)
    next_week_end = next_week_start + timedelta(days=6)
    
    context = {
        'schedules': schedules,
        'now': now,
        'start_date': start_date,
        'end_date': end_date,
        'today': today,
        'this_week_start': start_of_week,
        'this_week_end': end_of_week,
        'next_week_start': next_week_start,
        'next_week_end': next_week_end,
    }
    
    return render(request, 'classes/schedule_list.html', context)


@user_passes_test(lambda u: u.is_staff)
def create_schedule(request):
    """Admin view to create a single class schedule"""
    if request.method == 'POST':
        form = ScheduleCreationForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            messages.success(request, f'Schedule created for {schedule.fitness_class.name} on {schedule.date}')
            return redirect('admin_schedule_list')
    else:
        form = ScheduleCreationForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'classes/create_schedule.html', context)


@user_passes_test(lambda u: u.is_staff)
def bulk_create_schedules(request):
    """Admin view to create recurring class schedules"""
    if request.method == 'POST':
        form = BulkScheduleCreationForm(request.POST)
        if form.is_valid():
            fitness_class = form.cleaned_data['fitness_class']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            days_of_week = [int(day) for day in form.cleaned_data['days_of_week']]
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            
            # Generate schedules for selected weekdays
            current_date = start_date
            created_count = 0
            
            while current_date <= end_date:
                if current_date.weekday() in days_of_week:
                    # Check if schedule already exists
                    if not ClassSchedule.objects.filter(
                        fitness_class=fitness_class,
                        date=current_date,
                        start_time=start_time
                    ).exists():
                        ClassSchedule.objects.create(
                            fitness_class=fitness_class,
                            date=current_date,
                            start_time=start_time,
                            end_time=end_time,
                            available_spots=fitness_class.max_capacity,
                            is_active=True
                        )
                        created_count += 1
                
                current_date += timedelta(days=1)
            
            messages.success(request, f'Successfully created {created_count} schedule(s) for {fitness_class.name}')
            return redirect('admin_schedule_list')
    else:
        form = BulkScheduleCreationForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'classes/bulk_create_schedules.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_schedule_list(request):
    """Admin view to manage all schedules"""
    schedules = ClassSchedule.objects.all().select_related(
        'fitness_class', 'fitness_class__category'
    ).order_by('-date', 'start_time')[:50]
    
    context = {
        'schedules': schedules,
    }
    
    return render(request, 'classes/admin_schedule_list.html', context)


@login_required
def add_class(request):
    """Add a fitness class (admin only)"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only administrators can do that.')
        return redirect('home')
    
    if request.method == 'POST':
        form = FitnessClassForm(request.POST, request.FILES)
        if form.is_valid():
            fitness_class = form.save()
            messages.success(request, f'Successfully added class: {fitness_class.name}')
            return redirect('class_detail', class_id=fitness_class.id)
        else:
            messages.error(request, 'Failed to add class. Please ensure the form is valid.')
    else:
        form = FitnessClassForm()
    
    template = 'classes/add_class.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)
