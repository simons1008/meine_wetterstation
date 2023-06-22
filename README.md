# Meine Wetterstation

Das Hauptprogramm meine_wetterstation.py liest periodisch Temperatur, Feuchte und Luftdruck von einem Sensor und zeigt sie auf dem lokalen Display an. Zusätzlich werden die gelesenen Daten und ihre Historie in einem Fenster des Web-Browsers dargestellt. 

Das Hauptprogramm und die importierten Module sind in Python geschrieben. Sie laufen auf einem ESP32 DevKit mit MicroPython und WLAN-Anbindung. 

Die HTML-Dateien enthalten HMTL-Code und JavaScript-Code, der vom Web-Browser ausgeführt wird. 

## Externe Hardware
- Sensorplatine: Auf der Sensorplatine befinden sich der BME280-Chip, ein Spannungsregler und ein Pegelwandler für die I2C-Schnittstelle.

- Displayplatine: Auf der Displayplatine befindet sich ein monochromes 0.96" OLED Display mit 128 x 64 Bildpunkten, die durch den verbauten SSD1306-Chip einzeln gesteuert werden. Der SSD1306-Chip hat eine I2C-Schnittstelle. 

## Vorbereitung
Zuerst wird das Modul geheim.py editiert. Hier werden die SSID und das Passwort des lokalen Netzwerks eingetragen. 

Anschließend werden das Hauptprogramm, alle Module und die HTML-Dateien mit einer geeigneten IDE (Thonny) in den Flash-Speicher des ESP32 DevKit geschrieben. Das Hauptprogramm bekommt den Namen main.py, damit es nach dem Reset automatisch ausgeführt wird. 

## Ausführung
Nach dem Reset baut das Hauptprogramm eine Verbindung zum lokalen Netzwerk auf und zeigt die SSID und die IP-Adresse auf dem lokalen Display. 

Danach wird der Web-Server gestartet und es werden Daten für die Web-Seiten log und hp (Homepage) bereitgestellt. 
Es folgt die periodische Ausführung von:
- Messung BME
- Temperatur in Liste schreiben
- Feuchte in Liste schreiben
- Daten für die Web-Seite wetter bereitstellen
- Daten für die Web-Seite temperatur bereitstellen
- Daten für die Web-Seite feuchte bereitstellen 
- Aktuelle Auslastung des ESP32 Speichers auf dem lokalen Display anzeigen
- Temperatur, Feuchte und Luftdruck auf dem lokalen Display anzeigen
- Warten (insgesamt 600 Sekunden = 10 Minuten)

## Darstellung der Historie im Web-Browser
Im Web-Browser gelangt man durch die Eingabe der IP-Adresse (siehe oben) auf die Homepage der Wetterstation. Dort gibt es Links zu den anderen Web-Seiten. 

Die Wetterstation stellt alle 10 Minuten neue Daten bereit. Die Historie der Temperatur- und Feuchte-Werte wird auf den entsprechenden Seiten übersichtlich in einem Diagramm dargestellt. Dabei steht der aktuelle Wert am rechten Rand und die Historie links davon. 

Wenn der ESP32 Speicher für die Darstellung der Historie nicht ausreicht, wird "Internal Server Error" angezeigt. Dann hilft ein erneuter Abruf der Web-Seite. 

Nach 24 Stunden Laufzeit enthalten die Listen 144 Temperatur-Werte und 144 Feuchte-Werte. Nach 24 Stunden ist ein Neustart des Programms (Neubeginn der Historie) empfehlenswert, weil dann "Internal Server Error" gehäuft auftritt. 

Wenn das Programm nicht neu gestartet wird, werden nach 24 Stunden Laufzeit nur die letzten 144 Werte angezeigt. 

## Quellen
Die Grundlage für dieses Projekt stammt von hier: https://www.youtube.com/@HobbyelektronikerCh Kurs "Micropython mit ESP32".
Änderungen:
| Micropython mit ESP32             | Meine Wetterstation                             |
| --------------------------------- | ----------------------------------------------- |
| Heltec Board                      | ESP32 DevKit und externes OLED Display          |
| Wetter von openweathermap.org     | Ausschließlich lokale Daten vom BME280          |
| Web-Seiten hp, log, wetter        | Web-Seiten hp, log, wetter, temperatur, feuchte |
| Python-Code und HTML-Code         | Python-Code, HTML-Code, JavaScript-Code         |

Die Grundlage für den JavaScript-Code stammt von hier: 
https://stackoverflow.com/questions/43388716/the-correct-way-to-graph-of-a-function-on-html5-canvas im Kommentar von Ozan https://jsfiddle.net/ozzan/2b3ns745/1/
Änderungen: 
| fiddle                            | Meine Wetterstation                              |
| --------------------------------- | ------------------------------------------------ |
| Gitternetz und Beschriftung       | Wertebereich von Temperatur und Feuchte          |
| Plot einer math. Funktion         | Plot eines Arrays                                |
| Statischer Plot                   | Dynamischer Plot, aktueller Wert am rechten Rand |

# Dank
Ich danke vor allem dem Autor "hobbyelektroniker" für seinen hervorragenden Kurs "Micropython mit ESP32". Der Kurs enthält Erklärungen und Lösungen auf vielen Gebieten. Eine (unvollständige) Aufzählung:
- Einrichtung der Entwicklungsumgebung
- Anzeige auf dem OLED-Display
- Messung mit dem BME280-Sensor
- WLAN-Verbindung
- UTC-Zeit aus dem Internet 
- Web-Server
- Erzeugung von Web-Seiten
- ESP32 Speicher und Garbage Collector

Dieser Kurs hat mein Projekt möglich gemacht!

Dann danke ich dem Autor "Ozan" für den JavaScript-Code in seinem fiddle. Der Code zeichnet auf HTML5 Canvas und benötigt keine Bibliothek.





