import display
import yahooweather
import time
import smogpollution
import weatherutils

LOCATION_CITY = "Wroclaw"
LOCATION_COUNTRY = "PL"


def refreshing_data_info():
    display.lcd_string_scroll("Odswiezam dane", display.LCD_LINE_1)
    display.lcd_string_scroll("Prosze czekac...", display.LCD_LINE_2)


def basic_info():
    display.lcd_string_scroll(weatherutils.date_time_string(), display.LCD_LINE_1)
    display.lcd_string_scroll(weatherutils.location_string(LOCATION_CITY, LOCATION_COUNTRY), display.LCD_LINE_2)


def error_info():
    display.lcd_string_scroll("Wystapil blad")
    display.lcd_string_scroll("Dane zostana pobrane ponownie")


def smog_info(smog_data):
    display.lcd_string_scroll(smog_data["PM10"], display.LCD_LINE_1)
    display.lcd_string_scroll(smog_data["PM25"], display.LCD_LINE_2)


def forecast_info(weather_data):
    display.lcd_string_scroll(weather_data["tomorrow_temperature"], display.LCD_LINE_1)
    display.lcd_string_scroll(weather_data["tomorrow_details"], display.LCD_LINE_2)


def weather_basic_info(weather_data):
    display.lcd_string_scroll(weather_data["temperature"], display.LCD_LINE_1)
    display.lcd_string_scroll(weather_data["details"], display.LCD_LINE_2)


def main():
    refresh_counter = 0
    display.lcd_init()

    weather_data = yahooweather.forecast(LOCATION_CITY, LOCATION_COUNTRY)
    smog_data = smogpollution.get_smog_data()

    while True:
        basic_info()
        time.sleep(5)

        if smog_data["error"]:
            error_info()
            time.sleep(5)
        else:
            smog_info(smog_data)
            time.sleep(5)

        if weather_data["error"]:
            error_info()
            time.sleep(5)
        else:
            weather_basic_info(weather_data)
            time.sleep(5)
            forecast_info(weather_data)
            time.sleep(5)

        refresh_counter += 1
        if refresh_counter == 100:
            refreshing_data_info()
            time.sleep(5)
            weather_data = yahooweather.forecast(LOCATION_CITY, LOCATION_COUNTRY)
            smog_data = smogpollution.get_smog_data()
            refresh_counter = 0


try:
    main()
finally:
    display.lcd_byte(0x01, display.LCD_CMD)
