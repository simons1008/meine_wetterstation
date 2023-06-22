''''' 
  Micropython mit ESP32
  Anzeige auf OLED
  
  Version 1.00, 28.12.2019
  Der Hobbyelektroniker
  https://community.hobbyelektroniker.ch
  https://www.youtube.com/c/HobbyelektronikerCh
  Der Code kann mit Quellenangabe frei verwendet werden.
  Geändert: I2C Pins, I2C durch SoftI2C ersetzt
            anzeigen_oled hinzugefügt              18.05.2023 (Si)
            Info über Speicher-Nutzung hinzugefügt 19.06.2023 (Si)
'''''

from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C  # Für Display
import gc                        # Für Info über die Speicher-Nutzung

# OLED Pins vereinbaren
i2c_oled = SoftI2C(scl=Pin(22), sda=Pin(21))
# OLED initialisieren
oled = SSD1306_I2C(128,64,i2c_oled)

# Hilfsfunktion für Display
def text_line(text, line, pos = 0):
    x = 10 * pos
    y = (line-1) * 11
    oled.fill_rect(x,y,128-10*pos,11,0) # Zeile löschen
    oled.text(text,x,y)                 # Text anzeigen
    
def anzeigen_oled(temp, feuchte, druck):
    oled.fill(0) # Bildschirm löschen   
    text_line("Temp.: {:5.1f} C".format(temp),1)
    text_line("Feuchte: {:3.0f} %".format(feuchte),3)
    text_line("Druck: {:5.0f} hPa".format(druck),5)
    oled.show()

def neue_daten():
    oled.fill(0) # Bildschirm löschen
    text_line("Memory ...",1)
    text_line("alloc: {}".format(gc.mem_alloc()),2)
    text_line("free : {}".format(gc.mem_free()),3)
    text_line("Neue Daten ...",5)
    oled.show()   