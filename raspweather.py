import display
import yahooweather
import time
import smogpollution
import weatherutils

REFRESH_RATE = 50

LOCATION_CITY = "Wroclaw"
LOCATION_COUNTRY = "PL"


def refreshing_data_info():
    display.lcd_string_scroll("Odswiezam dane", display.LCD_LINE_1)
    display.lcd_string_scroll("Prosze czekac...", display.LCD_LINE_2)
    time.sleep(5)


def basic_info():
    display.lcd_string_scroll(weatherutils.date_time_string(), display.LCD_LINE_1)
    display.lcd_string_scroll(weatherutils.location_string(LOCATION_CITY, LOCATION_COUNTRY), display.LCD_LINE_2)
    time.sleep(5)


def error_info():
    display.lcd_string_scroll("Wystapil blad", display.LCD_LINE_1)
    display.lcd_string_scroll("Dane zostana pobrane ponownie", display.LCD_LINE_2)


def smog_info(smog_data):
    if smog_data["error"] == 'true':
        error_info()
    else:
        display.lcd_string_scroll(smog_data["PM10"], display.LCD_LINE_1)
        display.lcd_string_scroll(smog_data["PM25"], display.LCD_LINE_2)
    time.sleep(5)


def forecast_info(weather_data):
    display.lcd_string_scroll(weather_data["tomorrow_temperature"], display.LCD_LINE_1)
    display.lcd_string_scroll(weather_data["tomorrow_details"], display.LCD_LINE_2)


def weather_basic_info(weather_data):
    if weather_data["error"] == 'true':
        error_info()
        time.sleep(5)
    else:
        display.lcd_string_scroll(weather_data["temperature"], display.LCD_LINE_1)
        display.lcd_string_scroll(weather_data["details"], display.LCD_LINE_2)
        time.sleep(5)
        forecast_info(weather_data)
        time.sleep(5)


def fetch_data():
    refresh_counter = 0
    weather_data = yahooweather.forecast(LOCATION_CITY, LOCATION_COUNTRY)
    smog_data = smogpollution.get_smog_data()
    return refresh_counter, smog_data, weather_data


def main():
    display.lcd_init()
    refresh_counter, smog_data, weather_data = fetch_data()

    while True:
        basic_info()
        smog_info(smog_data)
        weather_basic_info(weather_data)

        refresh_counter += 1
        if refresh_counter == REFRESH_RATE:
            refreshing_data_info()
            refresh_counter, smog_data, weather_data = fetch_data()


try:
    main()
finally:
    display.lcd_byte(0x01, display.LCD_CMD)
