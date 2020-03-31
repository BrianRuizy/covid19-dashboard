# ©Brian Ruiz, @brianruizy
# Created: 03-15-2020
import numpy as np
import pandas as pd
import datetime

# Datasets collected by JHU CSSE found in the following URL:
# https://github.com/CSSEGISandData/COVID-19 


def recent_file_date():
    # Returns date string of most recent file
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday = yesterday.strftime('%m-%d-%Y')
    file_date = yesterday
    return file_date


def daily_report(date_string = None):
    # Reports date as far back to 01-22-2020
    daily_report_dir = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    
    if date_string is None: 
        file_date = recent_file_date()
    else: 
        file_date = date_string 
    
    df = pd.read_csv(daily_report_dir + file_date + '.csv')
    return df


def confirmed_report():
    confirmed_time_series = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    df = pd.read_csv(confirmed_time_series)
    return df


def deaths_report():
    deaths_time_series = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
    df = pd.read_csv(deaths_time_series)
    return df


def recovered_report():
    recovered_time_series = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
    df = pd.read_csv(recovered_time_series)
    return df 
