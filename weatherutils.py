import time


def date_time_string():
    return "%s" % time.strftime("%d-%m-%Y %H:%M")


def today():
    return "%s" % time.strftime("%d-%m-%Y")


def location_string(city, country):
    return "%s, %s" % (city, country)