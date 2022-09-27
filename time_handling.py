"""A  module to convert a time into seconds and to get the current time"""
import time

def minutes_to_seconds( minutes: str ) -> int:
    """Converts minutes to seconds"""
    return int(minutes)*60

def hours_to_minutes( hours: str ) -> int:
    """Converts hours to minutes"""
    return int(hours)*60

def hhmm_to_seconds( hhmm: str ) -> int:
    """Converts hhmm to seconds"""
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])

def hhmmss_to_seconds( hhmmss: str ) -> int:
    """Converts hhmmss to seconds"""
    if len(hhmmss.split(':')) != 3:
        print('Incorrect format. Argument must be formatted as HH:MM:SS')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + \
        minutes_to_seconds(hhmmss.split(':')[1]) + int(hhmmss.split(':')[2])

def current_time_hhmm():
    """Gets the current time in hhmm"""
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)
