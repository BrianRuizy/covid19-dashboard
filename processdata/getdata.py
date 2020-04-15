# ©Brian Ruiz, @brianruizy
# Created: 03-15-2020
import numpy as np
import pandas as pd
import datetime
import locale

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
    # If passing arg, must use above date formatting '01-22-2020'
    daily_report_dir = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    
    if date_string is None: 
        file_date = recent_file_date()
    else: 
        file_date = date_string 
    
    df = pd.read_csv(daily_report_dir + file_date + '.csv')
    return df


def confirmed_report():
    # Returns time series version of cases confirmed globally
    confirmed_time_series = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    df = pd.read_csv(confirmed_time_series)
    return df


def deaths_report():
    # Returns time series version of deaths globally
    deaths_time_series = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    df = pd.read_csv(deaths_time_series)
    return df


def recovered_report():
    # Return time series version of recoveries globally
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
    
    if date_string is not None: 
        return growth_df.loc[growth_df.index == date_string]
    
    if weekly is True: 
        weekly_df = pd.DataFrame([])
        yesterday = pd.Timestamp('now').date() - pd.Timedelta(days=1)
        intervals = pd.date_range(end=yesterday, periods=8, freq='7D').strftime('%-m/%-d/%y').tolist()
        
        for day in intervals:
            weekly_df = weekly_df.append(growth_df.loc[growth_df.index==day])
            
        return weekly_df
    
    elif monthly is True:
        #TODO: finish implementation of monthly arg. 
        monthly_df = pd.DataFrame()
        growth_df = monthly_df

        
    return growth_df

def percentage_trends():
    """[summary]: Returns percantage of trend, relative to week prior delta
    Returns:
        [dataframe] -- [percentage objects]
    """    
    current = realtime_growth(weekly=True).iloc[-1]
    current['death_rate'] = (current.Deaths / current.Confirmed)*100
    last_week = realtime_growth(weekly=True).iloc[-2]
    last_week['death_rate'] = (last_week.Deaths / last_week.Confirmed)*100
    
    trends = round(number=((current - last_week)/last_week)*100, ndigits=1)
        
    return trends

