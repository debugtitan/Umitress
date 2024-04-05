from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('store.urls', namespace='store')),
    path('accounts/', include('accounts.urls', namespace='account')),
    path('Order/', include('Order.urls', namespace='order'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)