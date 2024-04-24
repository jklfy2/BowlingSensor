# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
#CLK  = 23
#MISO = 21
#MOSI = 19
#CS   = 20
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

check_interval = 0.5 # length of intervals
jam_threshold = 2 # how many intervals constitutes a jam
hand_threshold = 4 # how many intervals constitutes a hand entry
stopTime = [0]*8 # array of counters for how many "check_interval"s each sensor has been tripped
wasTripped = False # bool for sensor 3 (first hand entry sensor)
handTime = 0 # counter for hand entry logic
highLowThreshold = 1000 # would change for sensors likely, but this is what works for the buttons used to test, weeds out random values between 0 and 200

def checkBallJam(adc_value, channel):
    global stopTime
    global highLowThreshold
    if adc_value > highLowThreshold: 
        stopTime[channel] += 1
    else:
        stopTime[channel] = 0

    if stopTime[channel] >= jam_threshold/check_interval:
        print("\n----------------------  BALL  JAM  ----------------------\n") # this would be replaced with toggling a GPIO pin to actually stop the motor
    return

def checkHandEntry(adc_value_2, adc_value_3):
    # if channel 2 then channel 3 goes high (within 0.2 sec), stop the motor
    global wasTripped
    global handTime
    global highLowThreshold
    global hand_threshold
    if adc_value_3 > highLowThreshold: # if sensor 3 shows a value higher than the threshold
        wasTripped = True
        handTime = 0
    if wasTripped:
        handTime += 1 # increment counter
        if adc_value_2 > highLowThreshold: # if sensor 2 shows a value higher than the threshold
           print("\n-------------------- HAND  ENTRY --------------------\n") # this would be replaced with toggling a GPIO pin to actually stop the motor
    if handTime == hand_threshold: # if the counter expires
        handTime = 0 # reset counter
        wasTripped = False # reset trip value
    return

def main():
        print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
        print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
        print('-' * 57)
# Main program loop.
        while True:
    	# Read all the ADC channel values in a list.
                values = [0]*8
                for i in range(8):
        		# The read_adc function will get the value of the specified channel (0-7).
                        values[i] = mcp.read_adc(i)
    		# Print the ADC values.
                print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
                for i in range(2):
                        checkBallJam(values[i], i)
                checkHandEntry(values[2], values[3])
    		# Pause for half a second.
                time.sleep(check_interval)

if __name__ == "__main__":
        main()

