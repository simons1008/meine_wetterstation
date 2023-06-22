''' 
  Micropython mit ESP32
  - Verbindung mit WLAN,
  - Zeitzonen und aktuelle Zeit
  - Formatierung Zeit- und Datum
  
  Version 3.00, 01.07.2020
  Der Hobbyelektroniker
  https://community.hobbyelektroniker.ch
  https://www.youtube.com/c/HobbyelektronikerCh
  Der Code kann mit Quellenangabe frei verwendet werden.
'''

import network
import time
import socket
import ntptime
import urequests as requests

# Einbinden in das eigene WLAN
class WiFi:
    
    zeitzone = 7200 # Sommerzeit
    
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
    
    def get_wlan(self):
        return self.wlan
    
    def connect(self,ssid, passwort, timeout = 10000):
        self.wlan.active(False)
        while self.wlan.active():
            pass
        return self.fast_connect(ssid, passwort, timeout)       

    def fast_connect(self,ssid, passwort, timeout = 10000):
        #wenn eine fixe IP-Adresse benötigt wird:
        #self.wlan.ifconfig(('192.168.1.148', '255.255.255.0', '192.168.1.1', '192.168.1.1'))
        #IP, Netmask, Gateway, DNS
        self.wlan.active(True);
        self.wlan.connect(ssid,passwort)
        start = time.ticks_ms();
        while not self.wlan.isconnected() and start + timeout > time.ticks_ms():
            time.sleep(0.1)
        return self.wlan.isconnected()        

    def isconnected(self):
        return self.wlan.isconnected()
   
    def get_ip(self):
        conf = self.wlan.ifconfig() # (ip, subnet, gateway, dns)
        return conf[0]
    
    def get_ssid(self):
        return self.wlan.config('essid')
    
    def getRequest(self, url):
        return requests.get(url)

    ###### Zeit und Datum #######

    # Zeitverschiebung in Sekunden
    @classmethod
    def set_zeitzone(cls,zone):
        cls.zeitzone = zone    

    # Aktuelle Zeit
    # Sekunden seit 2000-01-01 00:00:00 UTC
    @classmethod
    def get_zeit(cls):
        try:
            ntptime.settime()
        except:
            return None
        return time.mktime(time.localtime())

    # Korrigiert 'zeit' um Zeitzone, wenn 'zeit' nicht mitgegeben
    # wird, wird die aktuelle Zeit zurückgegeben 
    @classmethod
    def get_zeit_lokal(cls, zeit = None):
        if zeit:
            return zeit + cls.zeitzone
        else:
            zeit = cls.get_zeit()
            if zeit:
                return zeit + cls.zeitzone
            else:
                return None

# Formatierungsfunktionen für Textausgabe
# von Datum und Zeit

# tt.mm.yyyy
def datum_text(zeit):
    zeitString = time.localtime(zeit)
    return "{:02d}.{:02d}.{:04d}".format(zeitString[2],zeitString[1],zeitString[0])

# hh:mm:ss
def zeit_text(zeit):
    zeitString = time.localtime(zeit)
    return "{:02d}:{:02d}:{:02d}".format(zeitString[3],zeitString[4],zeitString[5])

# tt.mm.yyyy hh:mm:ss
def datum_zeit_text(zeit):
    return datum_text(zeit) + " " + zeit_text(zeit)


    