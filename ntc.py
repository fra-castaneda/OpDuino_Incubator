import math

Vin = 5
Ro = 10000  # 10k Resistor # Steinhart Constants
# NTC_A
A1 = 0.0063442443241665146
B1 = -0.0003334849763062497    # https://rusefi.com/Steinhart-Hart.html
C1 = 1.1362000036815707e-7
# NTC_B
A2 = 0.006683038191418846
B2 = -0.0003447376947068032   # https://rusefi.com/Steinhart-Hart.html
C2 = -1.8985933131806144e-7

def thermistorRes(Vout):
    Rt = Ro / (1023 / Vout - 1)  # Arduino 1023   / 65535
    return Rt

def thermistorTempA(Vout):
    Rt = Ro / (1023 / Vout - 1)  # Arduino 1023   / 65535
    Temp = ((1 / (A1 + (B1 * math.log(Rt)) + C1 * math.pow(math.log(Rt), 3))) - 273.15)
    return Temp

def thermistorTempB(Vout):
    Rt = Ro / (1023 / Vout - 1)  # Arduino 1023   / 65535
    Temp = ((1 / (A2 + (B2 * math.log(Rt)) + C2 * math.pow(math.log(Rt), 3))) - 273.15)
    return Temp









