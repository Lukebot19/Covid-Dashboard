"""A module that handlers all of the covid data. From getting the API request to processing the CSV file

    Attributes
    ----------
    s ( sched ):
        The scheduler object that allows the program to store a queue of events and run them after a speficied time.
    updates ( list ):
        A list of all the updates that have been scheduled to happen by the user
    covid_data_list ( list ):
        A list of the current covid data with local_number_of_cases, local_current_number_of_hospital, local_cummulative_number_of_deaths,
        national_number_of_cases, national_current_number_of_hospital and national_cummulative_number_of_deaths. This gets updated after every update to the covid data. 
    schedules ( dictionary ):
        A dictionary that holds the active schedules that have been scheduled by the scheduler.
    
    Methods
    -------
    parse_csv_data(csv_filename):
        Function to open and return the contents of the CSV file
    process_covid_api_csv_data(covid_csv_data):
        Function to process the covid data from a variable
    process_covid_csv_data(covid_csv_data):
        Function for processing the csv file data
    covid_api_request(location="areaName=Exeter", location_type="areaType=ltla"):
        Function for requesting data from the api
    convert_csv_to_dict(contents):
        Function to convert the csv data into a dictionary
    schedule_covid_updates(update_interval, update_name, repeat, update_covid_tick, update_news_tick):
        Function to schedule a covid update
    get_s():
        A function to return the sched object
    remove_completed_update(what_to_remove):
        Function to remove an item from the update
    process_covid_dictionary_data(covid_dictionary_data):
        Function to process the covid dictionary data
    remove_from_update(what_to_remove):
        Function to remove an item from the update
    update_covid():
        Function to handler the update of the covid data to be displayed on the dashboard
    get_covid_data_list():
        Returns all of the covid data in a list
    update_updates(update_name, update_at, update_covid_tick, update_news_tick, repeating):
        Function to update the update function
    get_updates():
    Function to get the update list

"""
import sched
import time
import json
import logging
import sys
from uk_covid19 import Cov19API
from covid_news_handling import update_news


s = sched.scheduler(time.time, time.sleep)

updates = []
covid_data_list = []
schedules = {}

def parse_csv_data(csv_filename: str ) -> list:
    """Function to open and return the contents of the CSV file

        Parameters:
            csv_filename (str):
                The file name of the CSV file that is to be parsed.

        Returns:
            contents ( list ):
                A list of the content of the CSV file, where each line in an entry in the list

    """
    contents = []
    with open(csv_filename, 'r', encoding='cp1252') as file:
        contents = file.readlines()
    return contents

def process_covid_api_csv_data(covid_csv_data: list, local: bool) -> str:
    """Function to process the covid data from a list of data from the covid api
    
        Parameters:
            covid_csv_data ( list ):
                A list of the covid data from a CSV file, where each entry is one line of the CSV file
            local ( bool ):
                States if the data being requested is for the local or nation data

        Returns:
            number_of_cases ( int ):
                The number of covid cases from the data
            current_number_of_hospital ( int ):
                The number of people currently in hospital due to covid from the data
            cummulative_number_of_deaths ( int ):
                The total number of deaths due to covid from the data

    """
    again = True
    temp_num = 1
    number_of_cases = 0
    last_seven_strings = []
    cummulative_number_of_deaths = 0
    current_number_of_hospital = 0
    if local:
        last_seven_strings = covid_csv_data[2:9]
    else:
        last_seven_strings = covid_csv_data[3:10]
  
    for item in last_seven_strings:
        temp_list = item.split(',')
        number_of_cases += int(temp_list[6])
    for data in covid_csv_data[2::]:
        temp_death_list = data.split(',')
        if temp_death_list[0] != '\n':
            if temp_death_list[4] != '' and temp_death_list[4] != '\n':
                cummulative_number_of_deaths = int(temp_death_list[4])
                break
    while again:
        try:
            temp_list = covid_csv_data[temp_num].split(',')
            if temp_list[5] != '':
                current_number_of_hospital = int(temp_list[5])
                again = False
            else:
                temp_num += 1
        except:
            break
    return number_of_cases, current_number_of_hospital, cummulative_number_of_deaths

def process_covid_csv_data(covid_csv_data: list) -> str:
    """Function for processing the csv file data from a list where every entry is one row of the file
        
        Parameters:
            covid_csv_data ( list ):
                A list of the covid data from a CSV file, where each entry is one line of the CSV file

        Returns:
            number_of_cases ( int ):
                The number of covid cases from the data
            current_number_of_hospital ( int ):
                The number of people currently in hospital due to covid from the data
            cummulative_number_of_deaths ( int ):
                The total number of deaths due to covid from the data

    """
    number_of_cases = 0
    last_seven_strings = []
    cummulative_number_of_deaths = 0
    current_number_of_hospital = 0
    last_seven_strings = covid_csv_data[3:10]
    for item in last_seven_strings:
        temp_list = item.split(',')
        number_of_cases += int(temp_list[6])
    for data in covid_csv_data[2::]:
        temp_death_list = data.split(',')
        if temp_death_list[0] != '\n':
            if temp_death_list[4] != '' and temp_death_list[4] != '\n':
                cummulative_number_of_deaths = int(temp_death_list[4])
                break
    temp_list = covid_csv_data[1].split(',')
    if temp_list[5] != '':
        current_number_of_hospital = int(temp_list[5])
    return number_of_cases, current_number_of_hospital, cummulative_number_of_deaths

def covid_api_request(location: str = "areaName=Exeter", location_type: str = "areaType=ltla") -> dict:
    """Function for requesting data from the api
        
        Parameters:
            location ( str ):
                The location used in the api request to get the correct data
            location_type ( str ):
                The type of location, inputs include ltla, region, utla

        Returns:
            covid_dict ( dictionary ):
                A dictionary with the date as the key and add the data as the value

    """
    contents = []
    covid_dict = {}
    cases_and_deaths = {
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType" : "areaType",
    "date": "date",
    "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
    "hospitalCases": "hospitalCases",
    "newCasesBySpecimenDate": "newCasesBySpecimenDate",
    }
    try:
        logging.info('requesting data from covid api')
        api = Cov19API(filters=[location,location_type], structure=cases_and_deaths)
        api.get_csv(save_as="data.csv")
        contents = parse_csv_data("data.csv")
        covid_dict = convert_csv_to_dict(contents)
    except ConnectionError:
        logging.error('Connection Error')
        sys.exit()
    return covid_dict

def convert_csv_to_dict(contents: list) -> dict:
    """Function to convert the csv data into a dictionary
    
        Parameters:
            contents ( list ): The contents of the csv file where each entry is one line of the csv file

        Returns:
            covid_dict ( dictionary ): A dictionary with the date as the key and add the data as the value
    
    """
    covid_dict = {}
    for item in contents:
        if item != "\n":
            item = item.replace("\n", "")
            item = item.split(",")
            temp_date = item[3]
            item.pop(3)
            covid_dict[temp_date] = item
    return covid_dict

def schedule_covid_updates(update_interval: int, update_name: str, repeat: str='no', update_covid_tick: str='no',update_news_tick: str='no') -> None:
    """Function to schedule an update to the dashboard. It can update the covid data, and news articles either both together or seperatly, as well as scheduling updates to repeat every 24 hours
    
        Parameters:
                update_interval ( int ): 
                    The amount of time in seconds until the update should happen
                update_name ( str ):
                    The name of the update, this is the name that will appear at the top of the toast
                repeat ( str ):
                    States if the update schedule will be repeated every 24 hours. If it is 'repeat' the updatw will repeat, else it will only occour once
                update_covid_tick ( str ):
                    The string that states if it will update the covid data or not. If its 'covid-data', the covid data will update, else it wont.
                update_news_tick ( str ):
                    The string that states if it will update the news articles or not. If its 'news-data', the news articles will update, else it wont.

    """
    templist = []
    logging.debug(update_interval)
    if update_covid_tick == 'covid-data' and update_news_tick == 'news-data':
        e3 = s.enter(update_interval,2,update_news)
        logging.info("Added an event to update the news to the scheduler")
        e32 = s.enter(update_interval,1,update_covid)
        logging.info("Added an event to update the covd data to the scheduler")
        templist.append(e3)
        templist.append(e32)
    elif update_news_tick == 'news':
        e2 = s.enter(update_interval,2,update_news)
        logging.info("Added an event to update the news with the name "+ update_name +" to the scheduler")
        templist.append(e2)
    elif update_covid_tick == 'covid-data':
        e1 = s.enter(update_interval,1,update_covid)
        logging.info("Added an event to update the covid data with the name "+ update_name +" to the scheduler")
        templist.append(e1)

    if repeat != 'repeat':
        e4 = s.enter(update_interval,3, remove_completed_update, argument=(update_name, ))
        logging.info("Added an event to remove the toast for " + update_name + " to the scheduler")
        templist.append(e4)
    if repeat == 'repeat':
        e5 = s.enter(86400,4, schedule_covid_updates, argument=(update_interval, update_name, repeat, update_news_tick, update_covid_tick))
        logging.info("Added an event to reshedule an event "+ update_name +"to the scheduler")
        templist.append(e5)
    schedules[update_name] = templist



    s.run(blocking=False)
    logging.info("Scheduler set to run with blocking=False")

def get_s() -> sched:
    """A function to return the sched object
    
        Returns:
            s ( sched ): A schedule object that lets the program run schedule events

    """
    return s

def remove_completed_update(what_to_remove: str) -> None:
    """Function to remove an item from the update and schedules lists
    
        Parameters:
            what_to_remove ( str ): 
                The name of the update that will be removed from the updates and schedules lists
    
    """
    for keys in updates:
        if keys['title'] == what_to_remove:
            updates.remove(keys)
            logging.info('Removed a completed update from the updates list called: ' + what_to_remove)
            schedules.pop(what_to_remove)
            logging.info('Removed a completed update from the schedules list: ' + what_to_remove)

def process_covid_dictionary_data(covid_dictionary_data: dict) -> int:
    """Function to process the covid data from a dictionary to retrieve the number of cases, current number of hospital cases and the total number of deaths
    
        Parameters:
            covid_dictionary_data ( dictionary ) : 
                A dictionary of all the covid data

        Returns:
            number_of_cases ( int ): 
                The current number of cases in the region
            current_number_of_hospital ( int ): 
                The current number of people in hospital in the region
            cummulative_number_of_deaths ( int ): 
                The total number of deaths in the region  
    
    """
    number_of_cases = 0
    last_seven_strings = []
    cummulative_number_of_deaths = 0
    last_seven_strings = covid_dictionary_data[3:10]
    for item in last_seven_strings:
        temp_list = item.split(',')
        number_of_cases += int(temp_list[6])
    for data in covid_dictionary_data[2::]:
        temp_death_list = data.split(',')
        if temp_death_list[4] != '':
            cummulative_number_of_deaths = int(temp_death_list[4])
            break
    temp_list = covid_dictionary_data[1].split(',')
    current_number_of_hospital = int(temp_list[5])
    return number_of_cases, current_number_of_hospital, cummulative_number_of_deaths

def remove_from_update(what_to_remove: str) -> None:
    """Function to remove an item from the update list where the name of the the item is what_to_remove
    
        Parameters:
            what_to_remove ( str ): The name of the item that is going to be removed from the update lists
    
    """
    for keys in updates:
        if keys['title'] == what_to_remove:
            updates.remove(keys)
            #for value in schedules[what_to_remove]:
                #try:
                    #s.cancel(value)
                #except ValueError:
                    #logging.info('cannot cancel scheduled event: Because event doesnt exist')
            for number in range(len(schedules[what_to_remove])):
                if schedules[what_to_remove][number] is not None:
                    try:
                        s.cancel(schedules[what_to_remove][number])
                        logging.info('Successfully canncelled a scheduled event called ' + what_to_remove + 'at position '+ str(number))
                    except:
                        logging.error('ValueError: list.remove(x): x not in list')
            schedules.pop(what_to_remove)
            logging.info('Removed ' + what_to_remove + ' from the schedules list')

def update_covid() -> None:
    """Function to handler the update of the covid data to be displayed on the dashboard by requesting the up to date data from the covid api and adding it to the covid data list"""
    
    logging.info("updating covid")
    covid_data_list.clear()
    with open("config.json", 'r', encoding='cp1252') as json_data_file:
        data = json.load(json_data_file)
        location = 'areaName=' + data['area_name']
        area_type = 'areaType=' + data['location_type']
        covid_api_request(location, area_type)
    with open("config.json", 'r', encoding='cp1252') as json_data_file:
        data = json.load(json_data_file)
    content = parse_csv_data(data['covid_file_name'])
    local_number_of_cases, local_current_number_of_hospital, local_cummulative_number_of_deaths = process_covid_api_csv_data( content, True )
    covid_data_list.append(local_number_of_cases)
    covid_data_list.append(local_current_number_of_hospital)
    covid_data_list.append(local_cummulative_number_of_deaths)
    covid_api_request('areaName=England', 'areaType=nation')
    content = parse_csv_data('data.csv')
    national_number_of_cases, national_current_number_of_hospital, national_cummulative_number_of_deaths = process_covid_api_csv_data( content, False )
    covid_data_list.append(national_number_of_cases)
    covid_data_list.append(national_current_number_of_hospital)
    covid_data_list.append(national_cummulative_number_of_deaths)

def get_covid_data_list() -> list:
    """Returns all of the covid data in a list
    
        Returns:
            covid_data_list ( list ): A list that contains all of the covid data, where each entry is a type of data 
    """
    return covid_data_list

def update_updates(update_name:str, update_at:int, update_covid_tick:str, update_news_tick:str, repeating:str) -> None:
    """Function to update the updates list with all the content that the toats on the dashboard needs
    
        Parameters:
            update_name ( str ): 
                The name of the update that is to be added to the update list
            update_at ( int ): The
                The time at which the update will occour
            update_covid_tick ( str ): 
                States if the covid data will be updated, if it contains 'covid-data' covid data will be updated, else nothing will happen
            update_news_tick ( str ):
                States if the news articles will be updated, if it contains 'news-data' then news articles will be updated, else nothing will happen
            repeating ( str ):
                States if the update will repeat every 24 hours, if it is equal to 'repeat' then the word 'REPEATING' will be placed at the start of the content in the toast 
    
    """
    if update_name is not None and update_at is not None:
        update_dict = {}
        update_dict['title'] = update_name
        if update_covid_tick is not None and update_news_tick is not None:
            if repeating == 'repeat':
                update_dict['content'] = 'REPEATING: Updating covid and news at ' + update_at
                logging.info('Added ' + update_name + ' to the update dictionary')
            else:
                update_dict['content'] = 'Updating covid and news at ' + update_at
                logging.info('Added ' + update_name + ' to the update dictionary')
        elif update_covid_tick is not None:
            if repeating == 'repeat':
                update_dict['content'] = 'REPEATING: Updating covid at ' + update_at
                logging.info('Added ' + update_name + ' to the update dictionary')
            else:
                update_dict['content'] = 'Updating covid at ' + update_at
                logging.info('Added ' + update_name + ' to the update dictionary')
        elif update_news_tick is not None:
            if repeating == 'repeat':
                update_dict['content'] = 'REPEATING: Updating news at ' + update_at
                logging.info('Added ' + update_name + ' to the update dictionary')
            else:
                update_dict['content'] = 'Updating news at ' + update_at
                logging.info('Added ' + update_name + ' to the update dictionary')
                logging.info('Added ' + update_name + ' to the update dictionary')
        else:
            if repeating == 'repeat':
                update_dict['content'] = 'REPEATING: Updating nothing at ' + update_at
                logging.info('Added ' + update_name + ' to the update dictionary')
            else:
                update_dict['content'] = 'Updating nothing at ' + update_at
                logging.info('Added ' + update_name + ' to the update dictionary')
        updates.append(update_dict)

def get_updates() -> list:
    """Function to get the update list
    
        Returns:
            updates ( list ):
                A list of updates with all the content and titles that the toats on the dashboard need
    """
    return updates
