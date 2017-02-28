import json
import urllib
import urllib2
import weatherutils

HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}

ERROR_RESPONSE = "{'error':'true'}"


def prepare_url():
    return "https://demo.dacsystem.pl/dane-pomiarowe/pobierz"


def prepare_data(date):
    data = urllib.quote(
        '{"measType":"Auto","viewType":"Station","dateRange":"Day","date":"%s","viewTypeEntityId":"12","channels":[222, 223]}' % date)
    return "query=%s" % data


def adapt_json_response(json_response):
    response = json.loads(json_response)
    return {
        "PM10": "PM10: %s ug/m3" % weatherutils.format_smog(response["data"]["series"][0]["data"][-1][1]),
        "PM25": "PM2.5: %s ug/m3" % weatherutils.format_smog(response["data"]["series"][1]["data"][-1][1]),
        "error": "false"
    }


def get_smog_data():
    url = prepare_url()
    data = prepare_data(weatherutils.today())
    try:
        request = urllib2.Request(url, data, HEADERS)
        urlopen = urllib2.urlopen(request)
        response = urlopen.read()
        return adapt_json_response(response)
    except StandardError as e:
        return ERROR_RESPONSE


get_smog_data()
