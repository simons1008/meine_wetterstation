'''
  Erweiterte Funktionen und Fehlertoleranz
  Modifiziert für LoLin - Board
  Original in Lektion 19, Datei WebWetter9.py
  Geändert: Kein Wetter vom Netz, kein LoLin Board
            Stattdessen lokale Daten vom BME280          17.06.2023 (Si)
            Datenanzeige auf OLED Display                17.06.2023 (Si)
            Zusätzliche Webseite <temperature_history>   17.06.2023 (Si)
            Zusätzliche Webseite <humidity_history>      17.06.2023 (Si)
            Globale Variable program wird überschrieben  21.06.2023 (Si)
            Periodischer Aufruf von gc.collect()         21.06.2023 (Si)
'''

import sys
sys.path.append('/work')
from netzwerk import *
from geheim import *
from meine_webseiten import startHTTP, log, hp, wetter, temperature_history, humidity_history
from my_bme_rev1 import *
import display as disp
import time

# Initialisiere globale Variable für das JavaScript-Programm
program = 2500 * [" "] # die Programme sind kürzer als 2500 Bytes

# Initialisiere Listen für die Datenaufzeichnung
liste_1 = []
liste_2 = []
# DEBUG
# liste_1 = 72 * [31/3] + 72 * [121/3]
# liste_2 = 72 * [119/3] + 72 * [209/3]


# Erzeuge WiFi Instanz
wifi = WiFi()

def homepage():
    ip = wifi.get_ip()
    hp.add("Die ESP32 - Wetterstation kennt momentan folgende Funktionen:")
    hp.add()
    hp.add('Die aktuellen Messwerte: <a href="http://{}/wetter">http://{}/wetter</a>'.format(ip,ip))
    hp.add('Ein LOG als Debug-Hilfe beim Programmieren: <a href="http://{}/log">http://{}/log</a>'.format(ip,ip))
    hp.add('Aufgezeichnete Temperatur: <a href="http://{}/temperatur">http://{}/temperatur</a>'.format(ip,ip))
    hp.add('Aufgezeichnete Feuchte: <a href="http://{}/feuchte">http://{}/feuchte</a>'.format(ip,ip))

def anzeigen_wetter(temp, feuchte, druck):
    wetter.clear()
    wetter.add("Gelesen am {}".format(datum_zeit_text(wifi.get_zeit_lokal())))
    wetter.add("Temp.: {:5.1f} C".format(temp))
    wetter.add("Feuchte: {:3.0f} %".format(feuchte))
    wetter.add("Druck: {:5.0f} hPa".format(druck))
    
def anzeigen_temperature():
    global program
    with open("temperature_history.html") as datei:
        program = datei.read() 
    temperature_history.clear()
    temperature_history.add("Gelesen am {}".format(datum_zeit_text(wifi.get_zeit_lokal())))
    temperature_history.add("<script> array = {}; </script>".format(liste_1))
    temperature_history.add(program)
    
def anzeigen_humidity():
    global program
    with open("humidity_history.html") as datei:
        program = datei.read()
    humidity_history.clear()
    humidity_history.add("Gelesen am {}".format(datum_zeit_text(wifi.get_zeit_lokal())))
    humidity_history.add("<script> array = {}; </script>".format(liste_2))
    humidity_history.add(program)
 
disp.oled.fill(0) # Bildschirm löschen
disp.text_line("Mit Netzwerk",1)
disp.text_line("verbinden...",2)
disp.oled.show();
log.add_log("Mit WLAN verbinden...");

if wifi.connect(wlan_ssid,wlan_passwort):
    disp.oled.fill(0) # Bildschirm löschen
    disp.text_line(wifi.get_ssid(),1)
    disp.text_line(wifi.get_ip(),2)
    disp.oled.show()
    startHTTP()
    log.add_log("Mit {} verbunden, IP-Adresse {}".format(wifi.get_ssid(),wifi.get_ip()))
    homepage()
    log.add_log("Temperatur, Feuchte, Druck anzeigen");
    # Loop
    while True:        
        temp, feuchte, druck = messung_bme()     # Daten lesen
        liste_1.append(temp)                     # Temperatur in Liste schreiben
        liste_2.append(feuchte)                  # Feuchte in Liste schreiben
        anzeigen_wetter(temp, feuchte, druck)    # neue Daten zum Web-Server hinzufügen
        anzeigen_temperature()                   # javascript array zum Web-Server hinzufügen 
        anzeigen_humidity()                      # javascript array zum Web-Server hinzufügen
        gc.collect()                             # Speicher an den Heap zurückgeben
        disp.neue_daten()                        # neue Daten an OLED melden
        time.sleep(60)
        disp.anzeigen_oled(temp, feuchte, druck) # neue Daten auf OLED anzeigen
        time.sleep(540)
else:
    disp.oled.fill(0) # Bildschirm löschen
    disp.text_line("Kein Netzwerk",1)
    disp.text_line("gefunden!",2)
    disp.oled.show()
    log.add_log("Keine Verbindung möglich")
    log.print()
