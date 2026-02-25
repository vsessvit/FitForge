from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


def custom_404(request, exception=None):
    """Custom 404 error handler"""
    logger.warning(f'404 error: {request.path}')
    return render(request, '404.html', status=404)


def custom_500(request):
    """Custom 500 error handler"""
    logger.error(f'500 error: {request.path}')
    return render(request, '500.html', status=500)
