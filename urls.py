from django.contrib import admin
from django.urls import path
from pickups.views import hotspot_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hotspot_view, name='hotspot'),  # nossa view principal
]
