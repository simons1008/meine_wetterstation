''' 
  Micropython mit ESP32
  Messung Temperatur, Luftfeuchtigkeit und Luftdruck
  mit BME280, erster Versuch
  
  Version 1.11, 04.11.2019
  Der Hobbyelektroniker
  https://community.hobbyelektroniker.ch
  https://www.youtube.com/c/HobbyelektronikerCh
  Der Code kann mit Quellenangabe frei verwendet werden.
  Original in Lektion 8, Datei BME2.py
  barometer_faktor aus Lektion 11, Datei BME280_3.py
  Geändert: Verwendung von SoftI2C  06.05.2023 (Si)
            Loop auskommentiert     08.05.2023 (Si) 
'''

# Standardmodule
from machine import Pin, SoftI2C 
import time

# externe Module, müssen auf das Board kopiert werden
import bme280_i2c

# globale Variable
barometer_faktor = 1017/964 # Normierung auf Wetterstation FN

# BME280 Setup
i2c_bme = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
bme = bme280_i2c.BME280_I2C(0x76, i2c=i2c_bme)
bme.set_measurement_settings({
    'filter': bme280_i2c.BME280_FILTER_COEFF_OFF,
    'osr_h': bme280_i2c.BME280_OVERSAMPLING_1X,
    'osr_p': bme280_i2c.BME280_OVERSAMPLING_1X,
    'osr_t': bme280_i2c.BME280_OVERSAMPLING_1X})

# BME280 Funktionen  
# def anzeigen(temp, feuchte, druck):
#     print("Temp.: {:5.1f} C".format(temp));
#     print("Feuchte: {:3.0f} %".format(feuchte));
#     print("Druck: {:5.0f} hPa".format(druck));
#     print()

def messung_bme():
    bme.set_power_mode(bme280_i2c.BME280_FORCED_MODE)
    time.sleep_ms(40)
    resultat = bme.get_measurement()
    return resultat["temperature"], resultat["humidity"], barometer_faktor * resultat["pressure"] / 100

# Loop
# while 1:
    # temp, feuchte, druck = messung_bme()
    # anzeigen(temp, feuchte, druck)
    # time.sleep(10)
    # i += 1
