# ©Brian Ruiz, @brianruizy
# Created: 03-15-2020
import numpy as np
import pandas as pd
import datetime
import locale
import urllib.request
from urllib.error import HTTPError

# Datasets scraped can be found in the following URL's:
# https://github.com/CSSEGISandData/COVID-19 
# https://github.com/owid/covid-19-data/tree/master/public/data


def daily_report(date_string=None):
    # Reports aggegrade data, dating as far back to 01-22-2020
    # If passing arg, must use above date formatting '01-22-2020'
    report_directory = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    
    if date_string is None: 
        yesterday = datetime.date.today() - datetime.timedelta(days=2)
        file_date = yesterday.strftime('%m-%d-%Y')
    else: 
        file_date = date_string 
    
    df = pd.read_csv(report_directory + file_date + '.csv')
    return df

def daily_cases():
    # returns the daily reported cases for respective date, 
    # segmented globally and by country
    df = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/new_cases.csv')
    return df


def daily_deaths():
    # returns the daily reported deaths for respective date, 
    df = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/new_deaths.csv')
    return df


def confirmed_report():
    # Returns time series version of total cases confirmed globally
    confirmed_time_series = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    df = pd.read_csv(confirmed_time_series)
    return df


def deaths_report():
    # Returns time series version of total deaths globally
    deaths_time_series = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    df = pd.read_csv(deaths_time_series)
    return df


def recovered_report():
    # Return time series version of total recoveries globally
    recovered_time_series = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
    df = pd.read_csv(recovered_time_series)
    return df 


def realtime_growth(date_string=None, weekly=False, monthly=False):
    """[summary]: returns dataframe of real time global growth.
    If passing date_string argument, must use following date formatting '4/12/20'.
    Columns excluded with list comp. are: ['Province/State','Country/Region','Lat','Long'].

    Returns:
        [growth_df] -- [growth in series]
    """ 
    df1 = confirmed_report()[confirmed_report().columns[4:]].sum()
    df2 = deaths_report()[deaths_report().columns[4:]].sum()
    df3 = recovered_report()[recovered_report().columns[4:]].sum()
    
    growth_df = pd.DataFrame([])
    growth_df['Confirmed'], growth_df['Deaths'], growth_df['Recovered'] = df1, df2, df3
    growth_df.index = growth_df.index.rename('Date')
    yesterday = pd.Timestamp('now').date() - pd.Timedelta(days=1)
    
    if date_string is not None: 
        return growth_df.loc[growth_df.index == date_string]
    
    if weekly is True: 
        weekly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=8, freq='7D').strftime('%-m/%-d/%y').tolist()
        for day in intervals:
            weekly_df = weekly_df.append(growth_df.loc[growth_df.index==day])
        return weekly_df
    
    elif monthly is True:
        monthly_df = pd.DataFrame([])
        intervals = pd.date_range(end=yesterday, periods=3, freq='1M').strftime('%-m/%-d/%y').tolist()
        for day in intervals:
            monthly_df = monthly_df.append(growth_df.loc[growth_df.index==day])
        return monthly_df
    
    return growth_df


def percentage_trends():
    """[summary]: Returns percantage of trend, relative to week prior delta
    Returns:
        [dataframe] -- [percentage objects]
    """    
    current = realtime_growth(weekly=True).iloc[-1]
    last_week = realtime_growth(weekly=True).iloc[-2]
    trends = round(number=((current - last_week)/last_week)*100, ndigits=1)
    
    rate_change = round(((current.Deaths/current.Confirmed)*100)-((last_week.Deaths / last_week.Confirmed)*100), ndigits=2)
    trends = trends.append(pd.Series(data=rate_change, index=['Death_rate']))
    
    return trends


def cases_table():
    df = daily_report()[['Country_Region', 'Confirmed', 'Deaths', 'Recovered', 'Active']]
    df.rename(columns={'Country_Region':'Country'}, inplace=True) 
    df = df.groupby('Country', as_index=False).sum()
    df.sort_values(by=['Confirmed'], ascending=False, inplace=True)
    
        
    return df

    # df['Death_Rate'] = round((df['Deaths']/df['Confirmed'])*100, ndigits=2)
