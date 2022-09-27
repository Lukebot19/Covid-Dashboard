_________________
CONTENTS OF THIS FILE
---------------------

 * [Introduction](#introduction)
 * [Prereqquisites](#prerequisites)
 * [Installation](#installation)
 * [Getting started](#getting-started)
 * [Testing](#testing)
 * [Developer Documentation](#developer-documentation)
 * [Details](#details)
_________________
 INTRODUCTION
------------

This program is a python backend that locally run and manage a web server, where a web page is built from a HTML template to display a dashboard.

This is a Covid-19 dashboard that allows you to view the latest covid figures from seven day infection rate to total deaths, on a local and national level. As well as that you can see all the latest news from across the world relating to covid and coronavirus. You can also schedule updates to be able to refresh the articles and covid data at a specified time. Both of these can be updated at the same time, or seperatly. If you want an update to happen every 24 hours you can make is a repeat update, and even 24 hours that same update will happen.

In addition to this, you can delete articles if you have read them and they wont reappear when an update occours making sure you only see new news articles. In a similar fashion you can delete any scheduled update that you dont want to happen 

This program was created as part of a coursework project as part of the module ECM1400-Programming.
_________________

Prerequisites
------------

A stable internet connection is required thoughout the operation of the program in order to retreive data from the APIs.


This program requires the following modules to be installed:

 * [Covid-19 API](https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/pages/getting_started.html#installation)

 Install the api by typing the following in the command line:
 ```
    python -m pip install uk-covid19
 ```


 * [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/)

 Install the flask environment by typing the following in the command line:
 ```
    pip install Flask
 ``` 

 This project was built and tested with python version: 3.9.9

 _________________
 INSTALLATION
 -------------------

 Before running the program head to the news api and get an API key. 
 * [News API](https://newsapi.org)

    * This api key can be placed in the *config.json* under the "api_key" field.

    * In addition to this, you can add which city you want the local covid data to be about under the "area_name" field

 In order to run the program use the command in the project directory that you unzipped the program to:

 ```
    main.py
 ```

Once you have done this, go to the following website on any web browser:

```
    http://127.0.0.1:5000
```

This will load the interface for the application that you can interact with.
_________________

GETTING STARTED
-------------------

Once you are on the interface there is a selection of different things you can do:

* Reading the data:

    * The top entry is the local 7-day infection rate in the city you specified in the config.json file.

    * Then the national 7-day infection rate in England

    * Then hospital cases in England

    * Then total deaths in England

* Scheduling an update:

    * In the first bar, you can input the time that you want the update to occour. This is an a 24 hour time format.

    * In the Update label box, input the name of the update. This will be displayed at the top of the toast widget.

    * The Repeat Update tick box tells the program if you want the update to occour every 24 hours. Tick this box if you want it to repeat, or leave it unticked if you want it to be a one off update

      * This will be indicated by a REPEATING: tag at the start of the content in the widget.

    * The Update Covid data tick box tells the program if you want to update the covid data during the scheduled update. Tick this box to indiced you want it to update.

    * The Update News articles tick box tells the program if you want to update the news articles during the scheduled update. Tick this box to indiced you want it to update.

    * If you tick both of these boxes then both the news articles and covid data will be updated during the scheduled update

* Removing news articles:

    * News articles can be removed by clicking on the x in the top right of the widget. This removes the toast and it will not return, even when the news is updated. This is a way to make sure you only see new news articles when it is updated.

* Removing scheduled updates

    * You can remove scheduled updates by clicking the x in the top right of the toast. This will cancel the scheduled update and it will not happen. If this update was a repeating update, it will also cancel all future update.
_________________
TESTING
--------

In order to test the program you need to run the 3 different test files.
 
* test_module.py

    *   This tests the parse_csv_data() function and the process_covid_csv_data() function from the covid_data_handler module.

* test_news_data_handling.py

    * This tests the news_API_request() function and the update_news() function in the covid_news_handling.py module.

* test_covid_data_handling.py

    * This tests the covid_API_request() function, process_covid_csv_data() function and the parse_csv_data()) function from the covid_data_handler.py module.

If there tests appear to do nothing then it means the program is working as intended and no errors have occoured.

Tests created with [PyTest](https://docs.pytest.org/en/6.2.x/)
_________________

DEVELOPER DOCUMENTATION
-----------------------

## main.py

    This is the main module that runs the program, this is what is used to trigger the different updates and control when the web server is triggered by the user.

  ### home()

    The main flask function used to run the backend of the web server by filling in the variables in the html

    This function will be called every time a user accesses the web server though the url http://127.0.0.1:5000 followed by "/" or "/index". 

## covid_data_handler.py

    A module that handlers all of the covid data. From getting the API request to processing the CSV file

  ### parse_csv_data() 

    Function to open and return the contents of the CSV file

  ### process_covid_api_csv_data()

    Function to process the covid data from a list of data from the covid api

  ### process_covid_csv_data() 

    Function for processing the csv file data from a list where every entry is one row of the file

  ### covid_api_request() 

    Function for requesting data from the api

  ### convert_csv_to_dict() 

    Function to convert the csv data into a dictionary

  ### schedule_covid_updates()

    Function to schedule an update to the dashboard. It can update the covid data, and news articles either both together or seperatly, as well as scheduling updates to repeat every 24 hours

  ### get_s()

    A function to return the sched object

  ### remove_completed_update()

    Function to remove an item from the update and schedules lists

  ### process_covid_dictionary_data()

    Function to process the covid data from a dictionary to retrieve the number of cases, current number of hospital cases and the total number of deaths

  ### remove_from_update()

    Function to remove an item from the update list where the name of the the item is what_to_remove

  ### update_covid()

    Function to handler the update of the covid data to be displayed on the dashboard by requesting the up to date data from the covid api and adding it to the covid data list

  ### get_covid_data_list()

    Returns all of the covid data in a list

  ### update_updates()

    Function to update the updates list with all the content that the toats on the dashboard needs

  ### get_updates()

    Function to get the update list

## covid_news_handling.py 

    Module to manage the news on the dashboard from updating the articles to displaying the toasts on the right side of the screen.

  ### news_api_request()

    Function to get the news data from the news api

  ### get_articles()

    Function to return the articles list that contains all of the articles from the news api that the users hasnt deleted yet

  ### update_news()

    Function to update the news when the user requests or the dashboard refreshes

  ### remove_from_articles()

    Function to remove an item from the article dictionary


The program also uses a config file to set up some of the fundamental parts of the dashboard such as api keys, location names and type, as well as the name of the csv file the program saves all the data too. 

There is also a module called time_handling.py that can convert the current time and any given time into seconds from an hhmm format. This can be used to work out how long it is in seconds until a given time. The program uses this to work out how long until the scheduled update needs to happen.

_________________

DETAILS
--------

* Author: Luke Alexander

* License: 

      Copyright 2021 Luke Alexander

      Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

      The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

      THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

* Acknowledgements:

  [Covid-API](https://coronavirus.data.gov.uk/details/developers-guide/main-api)

  [Type-Hinting](https://docs.python.org/3/library/typing.html)

  [Logging-Basics](https://www.loggly.com/ultimate-guide/python-logging-basics/)

  [Some-bug-solving](https://blog.finxter.com/solved-typeerror-method-takes-1-positional-argument-but-2-were-given/)

  [Config-files](https://stackoverflow.com/questions/19379120/how-to-read-a-config-file-using-python)

  [Pylint](https://pylint.pycqa.org/en/latest/user_guide/run.html)