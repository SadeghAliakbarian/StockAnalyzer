from django.contrib import admin
from .models import Company, StockData, DashboardInfo

# Register your models here.
admin.site.register(Company)
admin.site.register(StockData)
admin.site.register(DashboardInfo)