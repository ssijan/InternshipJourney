from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('task0/', include('djangoViews.urls')),
    path('task1/', include('drfViews.urls')),
]
