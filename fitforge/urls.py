"""fitforge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from homepage import views as home_views
from . import views as fitforge_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('homepage.urls')),
    path('classes/', include('classes.urls')),
    path('memberships/', include('memberships.urls')),
    path('products/', include('products.urls')),
    path('bag/', include('bag.urls')),
    path('profile/', include('profiles.urls')),
    path('bookings/', include('bookings.urls')),
    path('checkout/', include('checkout.urls')),
    # Policy pages
    path('faq/', home_views.faq, name='faq'),
    path('terms/', home_views.terms, name='terms'),
    path('privacy/', home_views.privacy, name='privacy'),
    path('contact/', home_views.contact, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add test URLs only in DEBUG mode
if settings.DEBUG:
    urlpatterns += [
        path('test-500/', fitforge_views.test_500, name='test_500'),
    ]

# Custom error handlers
handler404 = 'fitforge.views.custom_404'
handler500 = 'fitforge.views.custom_500'
