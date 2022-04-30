from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.conf.urls import *

from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('TheaterManageMentApp/', include('TheaterManageMentApp.urls')),

    path('TheaterManageMent/', get_schema_view(
        title="TheaterManageMent",
    ), name='openapi-schema'),
    path('', TemplateView.as_view(
        template_name='index.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)