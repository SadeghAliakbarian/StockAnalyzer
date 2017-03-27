from __future__ import unicode_literals
from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=200)
    company_abbvr = models.CharField(max_length=10)
    description = models.TextField()
    company_data = models.FileField()

    #def __str__(self):
        #return self.company_name + ' (' + self.company_abbvr + ')'


class StockData(models.Model):
    stock_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    stock_date = models.DateField()
    stock_open = models.FloatField()
    stock_close = models.FloatField()
    stock_high = models.FloatField()
    stock_low = models.FloatField()
    stock_volume = models.BigIntegerField()

    #def __str__(self):
        #return self.stock_company + ' at ' + str(self.stock_date)

class DashboardInfo(models.Model):
    CHART_TYPE= (
        ('line', 'line'),
        ('pie', 'pie'),
        ('scatter', 'scatter'),
        ('column', 'column'),
    )
    X_AXIS = (
        ('stock_volume', 'stock_volume'),
        ('stock_date', 'stock_date'),
        ('stock_low', 'stock_low'),
        ('stock_high', 'stock_high'),
        ('stock_close', 'stock_close'),
        ('stock_open', 'stock_open'),
    )
    dashboard_company_abbreviation = models.CharField(max_length=100)
    dashboard_chart_type = models.CharField(max_length=100, choices=CHART_TYPE)
    dashboard_chart_xaxis = models.CharField(max_length=200, choices=X_AXIS)
    dashboard_chart_yaxis = models.CharField(max_length=500)
    dashboard_chart_xlabel = models.CharField(max_length=200)
    dashboard_chart_title = models.CharField(max_length=200)
