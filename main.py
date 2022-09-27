"""
main.py
===================================

The main module used to run the program

    Attributes
    ----------
    app : Flask
        An instance of the flask application that can be @ with the route of the url.


    Methods
    -------
    home() -> render_template()
        The main flask function used to run the backend of the web server by filling in the variables in the html
"""

import json
import logging
import pylint.lint
from flask import Flask, render_template, request
from time_handling import hhmm_to_seconds, current_time_hhmm
from covid_data_handler import schedule_covid_updates, get_covid_data_list, update_covid, update_updates, get_updates, remove_from_update, get_s
from covid_news_handling import update_news, remove_from_articles, get_articles


FORMAT =  '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig( filename='pysys.log',level=logging.DEBUG,format=FORMAT )

pylint_opts = ['--disable=line-too-long', 'covid_news_handling.py']
#pylint.lint.Run( pylint_opts )

app = Flask( __name__ )

update_covid()
update_news()

@app.route( "/" )
@app.route( "/index" )
def home() -> str:
    """The main flask function used to run the backend of the web server by filling in the variables in the html

    Returns: 
        Render template( Function ): A function that renders the template to the web server, which take a number of arguments.
    """
    logging.info( "Refreshing the webpage backend" )
    main_s = get_s()
    main_s.run( blocking=False )
    logging.info( "Scheduler set to run with blocking=False" )
    covid_data = get_covid_data_list()
    national_number_of_cases = covid_data[3]
    national_current_number_of_hospital = covid_data[4]
    national_cummulative_number_of_deaths = covid_data[5]
    local_number_of_cases = covid_data[0]
    notif = request.args.get( "notif" )
    logging.info('notif value: ' + str(notif))
    update_at = request.args.get( "update" )
    logging.info('update at value: ' + str(update_at))
    update_covid_tick = request.args.get( "covid-data" )
    logging.info('Update tick value ' + str(update_covid_tick))
    update_news_tick = request.args.get( "news" )
    logging.info('Update news tick value: ' + str(update_news_tick))
    repeat = request.args.get( "repeat" )
    logging.info('Repeat value '+ str(repeat))
    update_name = request.args.get( "two" )
    logging.info('Update name value '+ str(update_name))
    if update_name is not None and update_at is not None:
        update_updates( update_name, update_at, update_covid_tick, update_news_tick, repeat )
        time = (hhmm_to_seconds( update_at ) - hhmm_to_seconds( current_time_hhmm() ))
        if time <= 0:
            time = 86400 - abs( time )
        logging.info('seconds until update ' + str(time))
        schedule_covid_updates( time, update_name, repeat, update_covid_tick, update_news_tick )
    update_item = request.args.get( "update_item" )
    if update_item is not None:
        remove_from_update( update_item )
    articles = get_articles()
    if notif is not None:
        remove_from_articles( notif )
    update_list = get_updates()
    with open( "config.json", 'r', encoding='cp1252' ) as json_data_file:
        data = json.load( json_data_file )
        location_thing = data["area_name"]
    logging.info('Starting the render of the template')
    return render_template( "index.html", title='Covid Title',
     news_articles = articles,
      notification = 'news_dictionary',
      location = location_thing,
      updates = update_list,
      nation_location = 'England',
      national_7day_infections = national_number_of_cases,
      hospital_cases = 'Hospital cases: '+ str(national_current_number_of_hospital),
      deaths_total = 'Total deaths: ' + str(national_cummulative_number_of_deaths),
      local_7day_infections = local_number_of_cases,
      image = 'Coronavirus_Covid-19.png',
      favicon = 'static/images/coronavirus-5107715_1280.png'
      )

if __name__ == "__main__":
    app.run()
        