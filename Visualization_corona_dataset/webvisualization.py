#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from webvisualization_plots import plot_reported_cases_per_million, get_countries
from typing import Optional
from fastapi.responses import Response

# create app variable (FastAPI instance)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# mount one or more static directories,
# e.g. your auto-generated Sphinx documentation with html files
app.mount(
    # the URL where these files will be available
    "/static",
    StaticFiles(
        # the directory the files are in
        directory="static/",
        html=True,
    ),
    # an internal name for FastAPI
    name="static",
)

@app.get("/")
def plot_reported_cases_per_million_html(request: Request):
    """
    Root route for the web application.
    Handle requests that go to the path "/".
    """
    return templates.TemplateResponse(
        "plot_reported_cases_per_million.html",
        {
            "request": request,
            # Get list of countries present in the csv file
            "countries": get_countries(),
        },
    )

@app.get("/plot_reported_cases_per_million.json")
def plot_reported_cases_per_million_json(countries: Optional[str] = None, start: Optional [str] = None, end: Optional [str] = None):
    """Return json chart from altair """
    
    # The web app detects the default start up as receiving inputs.To avoid ugly and confusing errors, set parameters to None when no explicit argument is given in app
    if countries == "":
        countries = None
    if countries:
        countries = countries.split(",")
    
    if start == '':
        "Set default start"
        start = '2021-05-29'

    if end == '':
        "Set default end"
        end = '2021-11-29'
    chart = plot_reported_cases_per_million(countries, start, end)
    return chart.to_dict()

def main():
    """Called when run as a script
    Should launch your web app
    """
    " Launch web app with uvicorn, on a local host"
    import uvicorn 
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
