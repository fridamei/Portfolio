#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import altair as alt
import pandas as pd
import os 
from os.path import exists
import sys

def get_data_from_csv(columns, countries=None, start=None, end=None):
    """Creates pandas dataframe from .csv file.
    Data will be filtered based on data column name, list of countries to be plotted and
    time frame chosen.
    Args:
        columns (list(string)): a list of data columns you want to include
        countries ((list(string), optional): List of countries you want to include.
        If none is passed, dataframe should be filtered for the 6 countries with the highest
        number of cases per million at the last current date available in the timeframe chosen.
        start (string, optional): The first date to include in the returned dataframe.
            If specified, records earlier than this will be excluded.
            Default: include earliest date
            Example format: "2021-10-10"
        end (string, optional): The latest date to include in the returned data frame.
            If specified, records later than this will be excluded.
            Example format: "2021-10-10"
    Returns:
        cases_df (dataframe): returns dataframe for the timeframe, columns, and countries chosen
    """
    # add path to .csv file from 6.0
    path = os.path.join(os.getcwd() + '/owid-covid-data.csv')

    # Check if file existss
    msg  = "No such file or directory"
    assert exists(path), msg
	
    # read .csv file, define which columns to read
    df = pd.read_csv(
        path,
        sep=",",
        usecols=["location"] + ["date"] + columns,
        parse_dates=["date"],
        date_parser=lambda col: pd.to_datetime(col, format="%Y-%m-%d"),
    )
    
    if countries is None:
        # no countries specified, pick 6 countries with the highest case count at end_date
        if end is None:
            # no end date specified, pick latest date available
            end_date = df.date.iloc[-1]
        else:
            end_date = datetime.strptime(end, "%Y-%m-%d")
        df_latest_dates = df[df.date.isin([end_date])]

        # identify the 6 countries with the highest case count
        # on the last included day
        # Make list of the first countries after sorting the dataframe in descending order after the value of columns, filtering out only the 'location' column and choosing the first 6 entries
        countries = df_latest_dates.sort_values(columns, ascending=False)['location'].head(6)

    # now filter to include only the selected countries
    # Includes only the values where the location column of the row is in the countries list (among the selected countries)
    cases_df = df[df.location.isin(countries)]
    
    # apply date filters
    if start is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        # exclude records earlier than start_date
        # Filters all cases where the statement inside the outer brackets evaluates to True (i.e. where the date is equal to or more recent than start)
        cases_df = cases_df[cases_df['date'] >= start]

    if end is not None:
        end_date = datetime.strptime(end, "%Y-%m-%d")
        if start_date is not None and start_date >= end_date:
            raise ValueError("The start date must be earlier than the end date.")

        # exclude records later than end date
        cases_df = cases_df[cases_df['date'] <= end]

    return cases_df


def plot_reported_cases_per_million(countries=None, start=None, end=None):
    """Plots data of reported covid-19 cases per million using altair.
    Calls the function get_data_from_csv to receive a dataframe used for plotting.
    Args:
        countries ((list(string), optional): List of countries you want to filter.
        If none is passed, dataframe will be filtered for the 6 countries with the highest
        number of cases per million at the last current date available in the timeframe chosen.
        start (string, optional): a string of the start date of the table, none
        of the dates will be older than this on
        end (string, optional): a string of the end date of the table, none of
        the dates will be newer than this one
    Returns:
        altair Chart of number of reported covid-19 cases over time.
    """
    # choose data column to be extracted
    columns = ['new_cases_per_million']
    
    
    # create dataframe
      
    cases_df = get_data_from_csv(columns, countries, start, end) 

    # Note: when you want to plot all countries simultaneously while enabling checkboxes, you might need to disable altairs max row limit by commenting in the following line
    alt.data_transformers.disable_max_rows()

    chart = (
        alt.Chart(cases_df, title='Daily new confirmed COVID-19 cases per million people')
        .mark_line()
        .encode(
            x=alt.X(
                "date:T",
                axis=alt.Axis(
                    format="%b, %Y", title="Date", titleFontSize=14, tickCount=20
                ),
            ),
            y=alt.Y(
                columns[0],
                axis=alt.Axis(
                    title="Number of Reported Cases per Million",
                    titleFontSize=14,
                    tickCount=10,
                ),
            ),
            color=alt.Color("location:N", legend=alt.Legend(title="Country")),
        )
        .interactive()
    )
    return chart

def get_countries():
    """
    Finds all the unique countries (locations) in the csv-file
    
    Returns:
        pandas series of unique locations
    """
    path = os.path.join(os.getcwd() + '/owid-covid-data.csv')
    df = pd.read_csv(path, usecols=["location"])
    
    return df.location.unique()
   

def main(save=False):
    """Function called when run as a script
    Creates a chart and display it or save it to a file
    """
    "Set default values when script is run as main (task 6.2)"
    countries = ['Norway', 'Denmark', 'Sweden']
    start = '2021-05-29'
    end = '2021-11-29'
    chart = plot_reported_cases_per_million(countries, start, end)
    # chart.show requires altair_viewer
    # Saves the chart to HTML file if save is set to True
    if save:
        print("Saved chart as 'covid-plot.html'")
        chart.save('covid-plot.html')
    chart.show()

if __name__ == "__main__":
    save = False
    # Check if arguments are given (besides the script itself)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'save':
            # Save to disc if specified
            save = True
    
    main(save)
