# Visualization of the corona dataset
I ran the code in Anaconda Spyder 5 with python 3.8 on a Windows 10 comuputer, tested on VMWare Horizon remote from ifi workspace with python 3 running Linux Redhat.
Packages as run on the ifi server are described in requirements.txt file

## Task 6.1

### Dependencies
altair
altair_viewer
pandas
os

### Functionality
Uses the csv file downloaded from https://ourworldindata.org/covid-cases and plots the reported number of new cases of covid per day per country using pandas and altair.
The default values (the values specified in main() per delivery time, the functions default values are None) are as follows:
   countries: Norway, Sweden, Finland, Denmark
   Start date: '2021-05-29'
   End date: '2021-11-29' (last date in the set per download date)
   
   The plotted values are x = 'date' and y ='new_cases_per_million' 

If save is given as command line argument, the chart is saved to file

The csv file is stored as owid-covid-cases.csv

### Usage
Run the file from either terminal or in an IDE. 
```bash
python webvisualization_plots.py
```


or to save the chart:
```bash
python webvisualization_plots.py save
```

### Missing functionality
I interpreted the assigment text as it not being necessary to be able to set arguments (dates and countries) from command line, and so there is no support for that 

## Task 6.2
webvisualization.py
### Dependencies
uvicorn
all of the above

### Functionality
Uses the webvisualization_plots.py script, and FastAPI and uvicorn to display the generated plot on a local server as a web application. 

### Usage
Run the following command from the terminal:
```bash
python webvisualization.py
```

Enter `http://127.0.0.1:8000` in web browser to view the application

## Missing functionality
Arguments must be changed in the webvisualization_plots.
Got some errors (RuntimeError: asyncio.run() cannot be called from a running event loop) when I tried to run the script in both Spyder and Jupyter Notebook from my Windows computer, but worked as expected when run from the command line on the Ifi VmWare server.
As it worked on the Ifi computer, I did not spend too much time debugging the RuntimeError. 

## Task 6.3
webvisualization.py
### Dependencies
FastAPI
all of the above

### Functionality
Uses the webvisualization_plots.py script, and FastAPI and uvicorn to display the generated plot on a local server as a web application.
Check boxes to choose which countries to plot for and date inputs for start and end date (restricted to the limitations of the csv file) 
The default values for the countries are the six with the highest number of cases for the last day in the file.
The default dates are set in the webvisualization file, to 2021-05-29 and 2021-11-29, respectively
### Usage
Run the following command from the terminal:
```bash
python webvisualization.py
```

Enter `http://127.0.0.1:8000` in web browser to view the application

## Missing functionality
Arguments must be changed in the webvisualization_plots and webvisualization.py for the initial values for start and end dates to be plotted
