from django.urls import path
from . import views

app_name = 'BitcoinTransactions'
urlpatterns = [
    path('', views.bitcoin, name='bitcoin'),
    path('qr/<str:address>/', views.generate_qr, name='qr'),
]