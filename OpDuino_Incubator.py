import serial
import ntc
from pyA20.gpio import gpio
from pyA20.gpio import port
import dht11
import csv
import datetime
import time

PIN7 = port.PA6  # Room Temp Op GPIO 7
gpio.init()

# read data using selected pin
op_gpio7 = dht11.DHT11(pin=PIN7)  # Room Temperature
# Incubator_OpDuino_V2
arduino = serial.Serial('/dev/ttyUSB0', 9600)
pelt_on = 'A'  # Peltier A Arduino 13
pelt_off = 'a'
vent_on = 'B'  # Peltier B Arduino 12
vent_off = 'b'
init = 'ab'
Pelt = 'Inactive'
Vent = 'Active'
arduino.write(init.encode())

MaxTemp = 65
CultTemp = 20
MidTemp = CultTemp + 4

with open('OpDuino_Incubator.csv', 'a') as csvfile:
    field_names = ['DateTime', 'Date', 'Time', 'Temp1', 'Hum1', 'Temp2', 'Temp3', 'Temp4', 'Pelt', 'Vent']
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writerow(
        {'DateTime': 'DateTime', 'Date': 'Date', 'Time': 'Time',
         'Temp1': 'Temp1', 'Hum1': 'Hum1',
         'Temp2': 'Temp2', 'Temp3': 'Temp3', 'Temp4': 'Temp4', 'Pelt': 'Pelt', 'Vent': 'Vent'})
    while True:
        rightnow = datetime.datetime.now()
        Room = op_gpio7.read()  # Room Temp-Hum
        datastr = arduino.readline()
        lstdata = datastr.split()
        if len(lstdata) == 6:
            Ard_A0 = lstdata[0]  # Peltier Temp
            Ard_A1 = lstdata[1]  # Chamber Temp
            Ard_A2 = lstdata[2]  # Culture Temp
            if len(Ard_A0) >= 3:
                Temp2 = ntc.thermistorTempB(float(Ard_A0))
            if len(Ard_A1) >= 3:
                Temp3 = ntc.thermistorTempB(float(Ard_A1))
            if len(Ard_A2) >= 3:
                Temp4 = ntc.thermistorTempA(float(Ard_A2))
            print(rightnow.strftime("%d/%m/%Y"), rightnow.strftime("%H:%M:%S"), 'Room (C RH)',
                  round(Room.temperature, 1), round(Room.humidity, 1),
                  'Pelt (C)', round(Temp2, 1), 'Chamber (C)', round(Temp3, 1), 'Culture (C)', round(Temp4, 1),
                  'Pelt', Pelt, 'Vent', Vent)
            writer.writerow(
                {'DateTime': str(datetime.datetime.now()),
                 'Date': rightnow.strftime("%d/%m/%Y"), 'Time': rightnow.strftime("%H:%M:%S"),
                 'Temp1': Room.temperature, 'Hum1': Room.humidity, 'Temp2': Temp2,
                 'Temp3': Temp3, 'Temp4': Temp4, 'Pelt': Pelt, 'Vent': Pelt})
            csvfile.flush()
            arduino.reset_input_buffer()
            time.sleep(5)

            if Temp2 >= MaxTemp:  # Peltier Temp
                if 'Active' in Pelt:
                    arduino.write(pelt_off.encode())
                    Pelt = 'Inactive'
            elif Room.temperature >= (CultTemp - 2):  # Room Temp
                if 'Active' in Pelt:
                    arduino.write(pelt_off.encode())
                    Pelt = 'Inactive'

            elif Temp3 >= MidTemp:  # Chamber Temp
                if 'Active' in Pelt:
                    arduino.write(pelt_off.encode())
                    Pelt = 'Inactive'

            elif Temp4 < CultTemp:  # Culture Temp
                if 'Inactive' in Pelt:
                    arduino.write(pelt_on.encode())
                    Pelt = 'Active'
            else:
                arduino.write(pelt_off.encode())
                Pelt = 'Inactive'






