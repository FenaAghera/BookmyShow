from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import HttpResponse

def health_check(request):
    """Health check endpoint for Railway"""
    return HttpResponse("OK", status=200)

def root_redirect(request):
    """Root path that works even if database isn't ready"""
    try:
        return redirect('movies/')
    except Exception:
        # If redirect fails, just return OK for health check
        return HttpResponse("OK", status=200)

urlpatterns = [
    path('health/', health_check, name='health'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('movies/', include('movies.urls')),
    path('', root_redirect),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)