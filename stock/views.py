from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import  StockData, Company#, Dashboard
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .forms import CompanyForm, StockDataForm#, DashboardForm
import cv2


def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()
    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

# index
def index(request):
    a_list = Company.objects.all()
    context = {'company_list': a_list}
    return render(request, 'stock/index.html', context)
    #return render(request, 'stock/project.html', context)

# create company
DB_FILE_TYPES = ['csv']
def create_company(request):
    form = CompanyForm(request.POST or None, request.FILES or None)
    if form.is_valid():
            company = form.save(commit=False)
            company.company_name = request.POST['company_name']
            company.company_abbvr = request.POST['company_abbvr']
            company.description = request.POST['description']
            company.company_data = request.FILES['company_data']
            file_type = company.company_data.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in DB_FILE_TYPES:
                context = {
                    'company': company,
                    'form': form,
                    'error_message': 'database should have a .csv file type',
                }
                return render(request, 'stock/create_company.html', context)
            company.save()
            # add all the data in db into StockData localdatabase
            db_df = pd.DataFrame.from_csv(company.company_data,index_col=None)
            data = db_df.head(251)
            columns = data.columns
            data_list = []
            for i in range(251):
                temp = []
                for j in range(len(columns)):
                    list.insert(temp, j, data.iloc[i][data.columns[j]])
                list.insert(data_list, i, temp)
                temp_date = temp[0].split('-')
                year = '20'+temp_date[2]
                month =month_string_to_number(temp_date[1])
                day = temp_date[0].zfill(2)
                new_date = year+'-'+str(month).zfill(2)+'-'+day
                SD = StockData(stock_company = company, stock_date = new_date,stock_open = temp[1],
                               stock_high=temp[2], stock_low = temp[3], stock_close = temp[4],
                               stock_volume=temp[5])
                SD.save()
            # go to details page
            return render(request, 'stock/company_detail.html', {
                'company': company,
                'data': data_list,
                'columns': columns,
                'col_count': len(columns)
            })
    context = {
            "form": form,
    }
    return render(request, 'stock/create_company.html', context)


def company_detail(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    db_df = pd.DataFrame.from_csv(company.company_data, index_col=None)
    data = db_df.head(251)
    columns = data.columns
    data_list = []
    for i in range(251):
        temp = []
        for j in range(len(columns)):
            list.insert(temp, j, data.iloc[i][data.columns[j]])
        list.insert(data_list, i, temp)

    return render(request, 'stock/company_detail.html', {
        'company': company,
        'data':data_list,
        'columns': columns,
        'col_count': len(columns)
    })



# draw charts
from chartit import DataPool, Chart
def stock_chart_view(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    stock_data = StockData.objects.filter(stock_company = company)
    #Step 1: Create a DataPool with the data we want to retrieve.
    stock_data = \
        DataPool(
           series=
            [{'options': {
               'source': stock_data},
              'terms': [
                'stock_date',
                'stock_open',
                'stock_close',
                  'stock_high',
                  'stock_low',
                  'stock_volume']}
             ])

    #Step 2: Create the Chart object
    cht_line = Chart(
            datasource = stock_data,
            series_options =
              [
                  {'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'stock_date': [
                    'stock_high',
                    'stock_low',
                  ]
                  }}
              ],
            chart_options =
              {'title': {
                   'text': 'The value of low/high at each given date'},
               'xAxis': {
                    'title': {
                       'text': 'Date'}}})

    cht_line2 = Chart(
        datasource=stock_data,
        series_options=
        [
            {'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                    'stock_date': [
                        'stock_open',
                        'stock_close'
                    ]
                }}
        ],
        chart_options=
        {'title': {
            'text': 'The value of open/close at each given date'},
            'xAxis': {
                'title': {
                    'text': 'Date'}}})

    cht_pie = Chart(
        datasource=stock_data,
        series_options=
        [
            {'options': {
                'type': 'pie',
                'stacking': False},
                'terms': {
                    'stock_date': [
                        'stock_volume']
                }}
        ],
        chart_options=
        {'title': {
            'text': 'The volume at each given date'},
            'xAxis': {
                'title': {
                    'text': 'Date'}}})

    cht_column = Chart(
        datasource=stock_data,
        series_options=
        [
            {'options': {
                'type': 'column',
                'stacking': False},
                'terms': {
                    'stock_date': [
                        'stock_volume']
                }}
        ],
        chart_options=
        {'title': {
            'text': 'The volume at each given date'},
            'xAxis': {
                'title': {
                    'text': 'Date'}}})

    #Step 3: Send the chart object to the template.
    return render(request,'stock/stock_chart_view.html',{
        'stock_chart': [cht_line, cht_line2, cht_column]
    })


from .forms import DashboardInfoForm
from .models import DashboardInfo

def dashboard(request):
    form = DashboardInfoForm(request.POST)
    if form.is_valid():
        dashboard_company_abbreviation = request.POST['dashboard_company_abbreviation']
        dashboard_chart_type = request.POST['dashboard_chart_type']
        dashboard_chart_xaxis = request.POST['dashboard_chart_xaxis']
        dashboard_chart_yaxis = request.POST['dashboard_chart_yaxis']
        dashboard_chart_title = request.POST['dashboard_chart_title']
        dashboard_chart_xlabel = request.POST['dashboard_chart_xlabel']

        yaxis = dashboard_chart_yaxis.split()

        #dash = get_object_or_404(DashboardInfo, pk=1)
        company = get_object_or_404(Company, company_abbvr=dashboard_company_abbreviation)
        stock_data1 = StockData.objects.filter(stock_company = company)
        #Step 1: Create a DataPool with the data we want to retrieve.
        stock_data = \
            DataPool(
               series=
                [{'options': {
                   'source': stock_data1},
                  'terms': [
                    'stock_date',
                    'stock_open',
                    'stock_close',
                      'stock_high',
                      'stock_low',
                      'stock_volume']}
                 ])
        cht = Chart(
            datasource=stock_data,
            series_options=
            [
                {'options': {
                    'type': dashboard_chart_type,
                    'stacking': False},
                    'terms': {
                        dashboard_chart_xaxis: yaxis

                    }}
            ],
            chart_options=
            {'title': {
                'text': dashboard_chart_title},
                'xAxis': {
                    'title': {
                        'text': dashboard_chart_xlabel}}})

        # some facts
        stat_volume = stock_data1.values_list('stock_volume', flat=True)
        stat_open = stock_data1.values_list('stock_open', flat=True)
        stat_close = stock_data1.values_list('stock_close', flat=True)
        stat_low = stock_data1.values_list('stock_low', flat=True)
        stat_high = stock_data1.values_list('stock_high', flat=True)

        return render(request, 'stock/dashboard.html', {'stock_chart': cht,
                                                        'volume': [np.mean(np.array(stat_volume)), np.max(np.array(stat_volume)), np.min(np.array(stat_volume)), np.max(np.array(stat_volume))-np.min(np.array(stat_volume))],
                                                        'open': [np.mean(np.array(stat_open)), np.max(np.array(stat_open)), np.min(np.array(stat_open)), np.max(np.array(stat_open))-np.min(np.array(stat_open))],
                                                        'close': [np.mean(np.array(stat_close)), np.max(np.array(stat_close)), np.min(np.array(stat_close)), np.max(np.array(stat_close))-np.min(np.array(stat_close))],
                                                        'low': [np.mean(np.array(stat_low)), np.max(np.array(stat_low)), np.min(np.array(stat_low)), np.max(np.array(stat_low))-np.min(np.array(stat_low))],
                                                        'high': [np.mean(np.array(stat_high)), np.max(np.array(stat_high)), np.min(np.array(stat_high)), np.max(np.array(stat_high))-np.min(np.array(stat_high))],
                                                        })
    return render(request, 'stock/dashboard.html', {'form': form , 'stock_chart':[]})