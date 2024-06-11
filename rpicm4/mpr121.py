# Based on Arduino example by Jim Lindblom
# http://bildr.org/2011/05/mpr121_arduino/

import smbus

bus = smbus.SMBus(3)

# MPR121 Register Defines

MHD_R = 0x2B
NHD_R = 0x2C
NCL_R = 0x2D
FDL_R = 0x2E
MHD_F = 0x2F
NHD_F = 0x30
NCL_F = 0x31
FDL_F = 0x32
ELE0_T = 0x41
ELE0_R = 0x42
ELE1_T = 0x43
ELE1_R = 0x44
ELE2_T = 0x45
ELE2_R = 0x46
ELE3_T = 0x47
ELE3_R = 0x48
ELE4_T = 0x49
ELE4_R = 0x4A
ELE5_T = 0x4B
ELE5_R = 0x4C
ELE6_T = 0x4D
ELE6_R = 0x4E
ELE7_T = 0x4F
ELE7_R = 0x50
ELE8_T = 0x51
ELE8_R = 0x52
ELE9_T = 0x53
ELE9_R = 0x54
ELE10_T = 0x55
ELE10_R = 0x56
ELE11_T = 0x57
ELE11_R = 0x58
FIL_CFG = 0x5D
ELE_CFG = 0x5E
GPIO_CTRL0 = 0x73
GPIO_CTRL1 = 0x74
GPIO_DATA = 0x75
GPIO_DIR = 0x76
GPIO_EN = 0x77
GPIO_SET = 0x78
GPIO_CLEAR = 0x79
GPIO_TOGGLE = 0x7A
ATO_CFG0 = 0x7B
ATO_CFGU = 0x7D
ATO_CFGL = 0x7E
ATO_CFGT = 0x7F

# MPR121 Proximity Registers
PRO_T = 0x59 # Touch Threshold register address
PRO_R = 0x5A # Touch Threshold register address

PROX_MHDR = 0x36 # ELEPROX Max Half Delta Rising register address - 0xFF
PROX_NHDAR = 0x37 # ELEPROX Noise Half Delta Amount Rising register address - 0xFF
PROX_NCLR = 0x38 # ELEPROX Noise Count Limit Rising register address - 0x00
PROX_FDLR = 0x39 # ELEPROX Filter Delay Limit Rising register address - 0x00
PROX_MHDF = 0x3A # ELEPROX Max Half Delta Falling register address - 0x01
PROX_NHDAF = 0x3B # ELEPROX Noise Half Delta Amount Falling register address - 0x01
PROX_NCLF = 0x3C # ELEPROX Noise Count Limit Falling register address - 0xFF
PROX_NDLF = 0x3D # ELEPROX Filter Delay Limit Falling register address - 0xFF
PROX_DEB = 0x5B # ELEPROX Debounce register address

PROX_NHDAT = 0x3E # ELEPROX Noise Half Delta Amount Touched register address - 0x00
PROX_NCLT = 0x3F # ELEPROX Noise Count Limit Touched register address - 0x00
PROX_FDLT = 0x40 # ELEPROX Filter Delay Limit Touched register address - 0x00

# Global Constants

#TOU_THRESH = 0x06
#REL_THRESH = 0x0A
TOU_THRESH = 0x06
REL_THRESH = 0x0A
PROX_THRESH = 0x3f
PREL_THRESH = 0x3c

MPR121_ADDRESS = 0x5A

# Routines

def readData(address):
	MSB = bus.read_byte_data(address, 0x00)
	LSB = bus.read_byte_data(address, 0x01)

	#touchData = (MSB << 8) | LSB
	touchData = MSB;

	return touchData;

def readWordData(address):
        MSB = bus.read_word_data(address, 0x00)
        LSB = bus.read_word_data(address, 0x01)

        #touchData = (MSB << 8) | LSB
        touchData = MSB;

        return touchData;

def setup(address):

	bus.write_byte_data(address, ELE_CFG, 0x00)

	# Section A - Controls filtering when data is > baseline.
	 
	bus.write_byte_data(address, MHD_R, 0x01)
	bus.write_byte_data(address, NHD_R, 0x01)
	bus.write_byte_data(address, NCL_R, 0x00)
	bus.write_byte_data(address, FDL_R, 0x00)

	# Section Proximity Sensing
	bus.write_byte_data(address, PROX_MHDR, 0xFF)
	bus.write_byte_data(address, PROX_NHDAR, 0xFF)
	bus.write_byte_data(address, PROX_NCLR, 0x00)
	bus.write_byte_data(address, PROX_FDLR, 0x00)

	# Section B - Controls filtering when data is < baseline.

	bus.write_byte_data(address, MHD_F, 0x01)
	bus.write_byte_data(address, NHD_F, 0x01)
	bus.write_byte_data(address, NCL_F, 0xFF)
	bus.write_byte_data(address, FDL_F, 0x02)

	# Proximity Sensing
	bus.write_byte_data(address, PROX_MHDF, 0x01);
	bus.write_byte_data(address, PROX_NHDAF, 0x01);
	bus.write_byte_data(address, PROX_NCLF, 0xFF);
	bus.write_byte_data(address, PROX_NDLF, 0xFF);	

	#Section C - Sets touch and release thresholds for each electrode

	bus.write_byte_data(address, ELE0_T, TOU_THRESH)
	bus.write_byte_data(address, ELE0_R, REL_THRESH)

	bus.write_byte_data(address, ELE1_T, TOU_THRESH)
	bus.write_byte_data(address, ELE1_R, REL_THRESH)

	bus.write_byte_data(address, ELE2_T, TOU_THRESH)
	bus.write_byte_data(address, ELE2_R, REL_THRESH)

	bus.write_byte_data(address, ELE3_T, TOU_THRESH)
	bus.write_byte_data(address, ELE3_R, REL_THRESH)

	bus.write_byte_data(address, ELE4_T, TOU_THRESH)
	bus.write_byte_data(address, ELE4_R, REL_THRESH)

	bus.write_byte_data(address, ELE5_T, TOU_THRESH)
	bus.write_byte_data(address, ELE5_R, REL_THRESH)

	bus.write_byte_data(address, ELE6_T, TOU_THRESH)
	bus.write_byte_data(address, ELE6_R, REL_THRESH)

	bus.write_byte_data(address, ELE7_T, TOU_THRESH)
	bus.write_byte_data(address, ELE7_R, REL_THRESH)

	bus.write_byte_data(address, ELE8_T, TOU_THRESH)
	bus.write_byte_data(address, ELE8_R, REL_THRESH)

	bus.write_byte_data(address, ELE9_T, TOU_THRESH)
	bus.write_byte_data(address, ELE9_R, REL_THRESH)

	bus.write_byte_data(address, ELE10_T, TOU_THRESH)
	bus.write_byte_data(address, ELE10_R, REL_THRESH)

	bus.write_byte_data(address, ELE11_T, TOU_THRESH)
	bus.write_byte_data(address, ELE11_R, REL_THRESH)	

	# Section D - Set the Filter Configuration. Set ESI2

	bus.write_byte_data(address, FIL_CFG, 0x04)

	# Section E - Set proximity sensing threshold and release
	bus.write_byte_data(address, PRO_T, PROX_THRESH)   # sets the proximity sensor threshold
	bus.write_byte_data(address, PRO_R, PREL_THRESH)   # sets the proximity sensor release

	# Section F - Set proximity sensor debounce
	bus.write_byte_data(address, PROX_DEB, 0x50);  # PROX debounce

	# Section G - Set Auto Config and Auto Reconfig for prox sensing
	bus.write_byte_data(address, ATO_CFGU, 0xC9)  # USL = (Vdd-0.7)/vdd*256 = 0xC9 @3.3V   
	bus.write_byte_data(address, ATO_CFGL, 0x82)  # LSL = 0.65*USL = 0x82 @3.3V
	bus.write_byte_data(address, ATO_CFGT, 0xB5)  # Target = 0.9*USL = 0xB5 @3.3V
	bus.write_byte_data(address, ATO_CFG0, 0x0B)

	# Section H - Start listening to all electrodes and the proximity sensor
	#bus.write_byte_data(address, ELE_CFG, 0x0C)
	bus.write_byte_data(address, ELE_CFG, 0x3C)

# import RPi.GPIO as GPIO
# 
# def handle_touch(channel):
#     touchData = readWordData(MPR121_ADDRESS )
#     for i in range(13):
#         if (touchData & (1<<i)):
#             print(i)
# 
# 
# if __name__ == "__main__":
# 
#     GPIO.setmode(GPIO.BCM)
#         
#     # Add callback to pin 22 (interrupt)
#     GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#     
#     GPIO.add_event_detect(22, GPIO.FALLING, callback=handle_touch)
#   
#     # Init mpr121 touch sensor
#     TOU_THRESH = 0x30
#     REL_THRESH = 0x33
#     
#     PROX_THRESH = 0x3f
#     PREL_THRESH = 0x3c
# 
#     setup(MPR121_ADDRESS )
# 
# 
# 
#     while True:
#         pass
# 

    
    
    
    
    
