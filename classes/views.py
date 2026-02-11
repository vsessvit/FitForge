from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import FitnessClass, ClassCategory, ClassSchedule


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
