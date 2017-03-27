from django import forms
from django.contrib.auth.models import User
from .models import Company, StockData
from .models import DashboardInfo


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_abbvr',
                  'description', 'company_data']


class StockDataForm(forms.ModelForm):
    class Meta:
        model = StockData
        fields = ['stock_company', 'stock_date', 'stock_open',
                  'stock_close', 'stock_high', 'stock_low', 'stock_volume']


class DashboardInfoForm(forms.ModelForm):
    class Meta:
        model = DashboardInfo
        fields = ['dashboard_company_abbreviation','dashboard_chart_type',
                  'dashboard_chart_xaxis','dashboard_chart_yaxis',
                  'dashboard_chart_title','dashboard_chart_xlabel']
