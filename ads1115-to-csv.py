from datetime import datetime
import time
import board
import busio
import csv
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

# Data collection setup
SAMPLES = 1000 # 860 * 60 * 30 = 30 mins
RATE = 860 # Data rate must be one of 8, 16, 32, 64, 128, 250, 475, 860 samples per second

# Create the I2C bus with a fast frequency
i2c = busio.I2C(board.SCL, board.SDA, frequency = 400000)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create a sinlge ended channel on Pin 0-3
#   Max counts for ADS1115 = 32767
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

# ADC Configuration
# Programable gain:
#
#       GAIN    RANGE (V)
#       ----    ---------
#        2/3    +/- 6.144
#          1    +/- 4.096
#          2    +/- 2.048
#          4    +/- 1.024
#          8    +/- 0.512
#         16    +/- 0.256
ads.gain = 1
ads.data_rate = RATE
ads.mode = Mode.SINGLE

start = time.monotonic()

f = open("log.csv", "w", newline="")
c = csv.writer(f)

c.writerow(["Datetime", "chan0", "chan1", "chan2", "chan3"]) # List of fieldnames
for i in range(SAMPLES):
	c.writerow([datetime.now().isoformat(sep=' ', timespec='milliseconds'), "{:8.6f}".format(chan0.voltage), "{:8.6f}".format(chan1.voltage), "{:8.6f}".format(chan2.voltage), "{:8.6f}".format(chan3.voltage)])

f.close()

end = time.monotonic()
total_time = end - start

print("Time of capture: {}s".format(total_time))
print("Sample rate requested={} actual={}".format(RATE, SAMPLES / total_time))