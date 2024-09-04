from blogs.models import Blogs

def custom_context_processor(request):
    # Obtiene los últimos 5 blogs
    latest_blogs = Blogs.objects.order_by('-created_at')[:5]
    return {
        'latest_blogs': latest_blogs,
    }
from datetime import datetime

def current_datetime(request):
    now = datetime.now()
    return {
        'day_of_week': now.strftime('%A'), 
        'day_of_month': now.strftime('%d'), 
        'month_name': now.strftime('%B'),  
        'month_number': now.strftime('%m'), 
        'year_two_digits': now.strftime('%y'), 
        'year_four_digits': now.strftime('%Y'), 
    }