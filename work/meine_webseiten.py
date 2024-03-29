''' 
  Micropython mit ESP32
  Verbindung mit WLAN, RTC setzen und abfragen
  
  Version 1.2, 30.06.2020
  Der Hobbyelektroniker
  https://community.hobbyelektroniker.ch
  https://www.youtube.com/c/HobbyelektronikerCh
  Der Code kann mit Quellenangabe frei verwendet werden.
  - Die Log-Datei wird bei jedem Programmstart gelöscht
  Original in Lektion 19
  Geändert: Zusätzliche Webseite <temperature_history>     17.06.2023 (Si)
            Zusätzliche Webseite <humidity_history>        17.06.2023 (Si)
'''

from microWebSrv import MicroWebSrv
from netzwerk import *
import os

'''
  titel: wird als Überschrift und <title> eingesetzt
  content: der eigentliche Inhalt
  refresh: Refresh - Zeit in Sekunden
'''
def _html(titel,content,refresh):
    return """\
    <!DOCTYPE html>
    <html lang=de>
        <head>
            <meta charset="UTF-8" />
            <meta http-equiv="refresh" content="{}">
            <title>{}</title>
        </head>
        <body>
            <h1>{}</h1>
            <h3>
            {}
            </h3>
        </body>
    </html>
    """.format(refresh,titel,titel,content)
        

class BigScreen:
    
    '''
      titel: wird als Überschrift und <title> eingesetzt
      content: der eigentliche Inhalt
      refresh: Refresh - Zeit in Sekunden
      filename: Filename, falls Speicherung gewünscht
    '''
    def __init__(self,titel,refresh,filename=""):
        self.titel = titel
        self.refresh = refresh
        self.filename = filename
        self.lines = []
        self.clear()
        
    def get_version(self):
        return 120 # enstspricht Version 1.2
        
    '''
      Der Filname kann nachträglich gesetzt oder gelöscht werden.
      set_filename() ohne Angabe löscht den Filenamen.
      Die bereits geschriebenen Werte werden jeweils übernommen.
    '''
    def set_filename(self,filename=""):
        if self.filename != "":
            self.lines.clear()
            for line in self.read_lines_from_file():
                self.lines.append(line.rstrip())    
            os.remove(self.filename)
        else:
            with open(filename,"w") as file:
                for line in self.lines:
                  file.write(line + "\n")
            self.lines.clear()
        self.filename = filename
            
    def add_line_to_file(self, line=""):
        with open(self.filename,"a") as file:
            file.write(line + "\n")
                
    def read_lines_from_file(self):
        with open(self.filename,"r+") as file:
            return file.readlines()
    
    def clear_file(self):
        with open(self.filename,"w") as file:
            pass
   
    def set_refresh(self, refresh):
        self.refresh = refresh
     
    def add(self, line = ""):
        if (self.filename != ""):
            self.add_line_to_file(line)
        else:
            self.lines.append(line)
        
    def clear(self):
        self.lines.clear()
        if (self.filename != ""):
            self.clear_file()
        
    def print(self):        
        if (self.filename != ""):
            for line in self.read_lines_from_file():
                print(line.rstrip())
        else:
            for line in self.lines:
                print(line)
            
    def get_content(self):
        if (self.filename != ""):
            content = ""
            for line in self.read_lines_from_file():
                content += line.rstrip() + "<br>"
            return content
        else:
            content = ""
            for line in self.lines:
                content += line + "<br>"
            return content
    
    def getHTML(self):
        return _html(self.titel,self.get_content(),self.refresh)

    def add_log(self, line = ""):
        if line != "":
            zeit = WiFi.get_zeit_lokal()
            if zeit:
                self.add(datum_zeit_text(zeit) + " " + line)
            else:
                self.add("--.--.---- --:--:-- " + line)
        else:    
            self.add(line)

# BigScreen(titel, refresh)
log = BigScreen("LOG",30)
hp = BigScreen("ESP32 Wetterstation - Homepage",300)
wetter = BigScreen("ESP32 Wetterstation - die aktuellen Messwerte",300)
temperature_history = BigScreen("ESP32 Wetterstation - aufgezeichnete Temperatur",300)
humidity_history = BigScreen("ESP32 Wetterstation - aufgezeichnete Feuchte",300)

@MicroWebSrv.route('/log')
def _httpHandlerTest(httpClient, httpResponse) :
    httpResponse.WriteResponseOk( headers        = ({"Cache-Control": "no-cache"}),
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = log.getHTML())

@MicroWebSrv.route('/')
def _httpHandlerTest(httpClient, httpResponse) :
    httpResponse.WriteResponseOk( headers        = ({"Cache-Control": "no-cache"}),
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = hp.getHTML())

@MicroWebSrv.route('/wetter')
def _httpHandlerTest(httpClient, httpResponse) :
    httpResponse.WriteResponseOk( headers        = ({"Cache-Control": "no-cache"}),
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = wetter.getHTML())

@MicroWebSrv.route('/temperatur')
def _httpHandlerTest(httpClient, httpResponse) :
    httpResponse.WriteResponseOk( headers        = ({"Cache-Control": "no-cache"}),
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = temperature_history.getHTML())

@MicroWebSrv.route('/feuchte')
def _httpHandlerTest(httpClient, httpResponse) :
    httpResponse.WriteResponseOk( headers        = ({"Cache-Control": "no-cache"}),
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = humidity_history.getHTML())

def startHTTP():
    srv = MicroWebSrv(webPath='www/')
    srv.MaxWebSocketRecvLen = 256
    srv.WebSocketThreaded = True
    srv.Start(True)
    
    
    