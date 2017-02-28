from urllib import quote
import urllib2
import json


CONDITION_CODES = {
    "0": "tornado",
    "1": "burza tropikalna",
    "2": "huragan",
    "3": "ciezkie burze",
    "4": "burze",
    "5": "deszcz ze sniegiem",
    "6": "deszcz i deszcz ze sniegiem",
    "7": "snieg i deszcz ze sniegiem", "8": "marznaca mzawka",
    "9": "deszcz", "10": "marznacy deszcz",
    "11": "deszczyk", "12": "deszczyk",
    "13": "sniezek", "14": "deszczyk, lekki snieg",
    "15": "sniezek", "16": "snieg",
    "17": "grad", "18": "deszcz",
    "19": "pyl", "20": "mgla",
    "21": "smog", "22": "smog",
    "23": "porywisty wiatr",
    "24": "wietrzne",
    "25": "zimno",
    "26": "zachmurzenie",
    "27": "przewaga chmur (w nocy)",
    "28": "niewielkie zachmurzenie (dzien)",
    "29": "Czesciowe zachmurzenie (noc)",
    "30": "Czesciowe zachmurzenie (dzien)",
    "31": "przejrzyscie (w nocy)",
    "32": "slonecznie",
    "33": "pogodnie (night)",
    "34": "pogodnie (dzien)",
    "35": "mieszane deszcz i grad",
    "36": "goraco",
    "37": "burzowo",
    "38": "rozproszone burze",
    "39": "rozproszone burze",
    "40": "rozproszony deszczyk",
    "41": "intensywne opady sniegu",
    "42": "rozproszone opady sniegu",
    "43": "ciezki snieg",
    "44": "mgla",
    "45": "burza z deszczem",
    "46": "opady sniegu",
    "47": "burza",
    "3200": "niedostepne"
}


ERROR_RESPONSE = json.loads("{'error':'true'}")


def prepare_query(city, country):
    query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s, %s") and ' \
            'u="c"' % (city, country)
    return quote(query)


def prepare_url(city, country):
    return 'https://query.yahooapis.com/v1/public/yql' + "?q=" + prepare_query(city, country) + "&format=json"


def translate_condition(code):
    return CONDITION_CODES[code]


def get_the_weather(json_response):
    data = json.loads(json_response)['query']['results']['channel']
    temperature = "Temperatura: %sC" % (data['item']['condition']['temp'])
    details = "Wiatr: %s km/h, Wilgotnosc: %s%%, %s" % (
        data['wind']['speed'], data['atmosphere']['humidity'],
        translate_condition(data['item']['condition']['code']))
    tomorrow_temperature = "Jutro: %sC - %sC" % (
        data['item']['forecast'][1]['low'], data['item']['forecast'][1]['high'])
    tomorrow_details = "%s" % translate_condition(data['item']['forecast'][1]['code'])
    in2days_temperature = "Pojutrze: %sC - %sC" % (
        data['item']['forecast'][2]['low'], data['item']['forecast'][2]['high'])
    in2days_details = "%s" % translate_condition(data['item']['forecast'][2]['code'])
    return {
        "temperature": temperature,
        "details": details,
        "tomorrow_temperature": tomorrow_temperature,
        "tomorrow_details": tomorrow_details,
        "in2days_temperature": in2days_temperature,
        "in2days_details": in2days_details
    }


def forecast(city, country):
    url = prepare_url(city, country)
    try:
        urlopen = urllib2.urlopen(url)
        return get_the_weather(urlopen.read())
    except StandardError as e:
        return ERROR_RESPONSE
