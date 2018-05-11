from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('bitcoin/', include('BitcoinTransactions.urls')),
    path('admin/', admin.site.urls),
]
