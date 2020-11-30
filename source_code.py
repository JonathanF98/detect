#Possible shebang would go here

############################# IMPORTS & GLOBALS ################################
import subprocess
import serial			          #imports pySerial for comm with LCD
import RPi.GPIO as GPIO		#imports RPi.GPIO_NP to talk with GPIO pins
import time
ser = serial.Serial('/dev/ttyS1', 115200)
currentForm = 0					    #global variable that should follow the current LCD screen form
													#Make sure to keep track of this value as it will change
													#between functions

#FORM 1 INDEXES
FORM_1_INDEX			= bytearray(b'\x01')			#replace "index with hex code such as 00,01,1B, ETC."
NETWORK_DETECT_LED	 	= bytearray(b'\x00')
RF_DETECT_LED 			= bytearray(b'\x01')
FORM1_EXIT_LED 		  	= bytearray(b'\x02')
#FORM 2 INDEXES
FORM_2_INDEX			= bytearray(b'\x02')
NETWORK_STRING_0		= bytearray(b'\x00')
NETWORK_STRING_1	  	= bytearray(b'\x01')
NETWORK_STRING_2		= bytearray(b'\x02')
NETWORK_STRING_3		= bytearray(b'\x03')
NETWORK_STRING_4		= bytearray(b'\x04')
NETWORK_LED_0		    = bytearray(b'\x03')
NETWORK_LED_1	    	= bytearray(b'\x04')
NETWORK_LED_2	  	  	= bytearray(b'\x05')
NETWORK_LED_3			= bytearray(b'\x06')
NETWORK_LED_4		    = bytearray(b'\x07')
#FORM 3 INDEXES
FORM_3_INDEX			= bytearray(b'\x03')
ENTER_KEY_LED	    	= bytearray(b'\x14')
KEYPAD_LED_0	    	= bytearray(b'\x08')
KEYPAD_LED_1	  	  	= bytearray(b'\x09')
KEYPAD_LED_2		    = bytearray(b'\x0A')
KEYPAD_LED_3		    = bytearray(b'\x0B')
KEYPAD_LED_4		    = bytearray(b'\x0C')
KEYPAD_LED_5	    	= bytearray(b'\x0D')
KEYPAD_LED_6	  	  	= bytearray(b'\x0E')
KEYPAD_LED_7		    = bytearray(b'\x0F')
KEYPAD_LED_8		    = bytearray(b'\x10')
KEYPAD_LED_9		    = bytearray(b'\x11')
KEYPAD_LED_10		  	= bytearray(b'\x12')
KEYPAD_LED_11			= bytearray(b'\x13')
PASSWORD_STRING		  	= bytearray(b'\x05')
#FORM 4 INDEXES
FORM_4_INDEX			= bytearray(b'\x04')
MAC_ADDRESS_STRING_0	= bytearray(b'\x06')
DEVICE_STRING_0			= bytearray(b'\x07')
MAC_ADDRESS_STRING_1	= bytearray(b'\x08')
DEVICE_STRING_1			= bytearray(b'\x09')
MAC_ADDRESS_STRING_2	= bytearray(b'\x0A')
DEVICE_STRING_2			= bytearray(b'\x0B')
NEXT_FORM_LED_0 		= bytearray(b'\x15')

#FORM 5 INDEXES
FORM_5_INDEX			= bytearray(b'\x05')
MAC_ADDRESS_STRING_3	= bytearray(b'\x0C')
DEVICE_STRING_3			= bytearray(b'\x0D')
MAC_ADDRESS_STRING_4	= bytearray(b'\x0E')
DEVICE_STRING_4			= bytearray(b'\x0F')
MAC_ADDRESS_STRING_5	= bytearray(b'\x10')
DEVICE_STRING_5			= bytearray(b'\x11')
NEXT_FORM_LED_1 		= bytearray(b'\x16')

#FORM 6 INDEXES
FORM_6_INDEX			= bytearray(b'\x06')
MAC_ADDRESS_STRING_6	= bytearray(b'\x12')
DEVICE_STRING_6			= bytearray(b'\x13')
MAC_ADDRESS_STRING_7	= bytearray(b'\x14')
DEVICE_STRING_7			= bytearray(b'\x15')
MAC_ADDRESS_STRING_8	= bytearray(b'\x16')
DEVICE_STRING_8			= bytearray(b'\x17')
NEXT_FORM_LED_2 		= bytearray(b'\x17')

#FORM 7 INDEXES
FORM_7_INDEX			= bytearray(b'\x07')
PROXIMITY_LED_0			= bytearray(b'\x18')
PROXIMITY_LED_1			= bytearray(b'\x19')
PROXIMITY_LED_2			= bytearray(b'\x1A')
PROXIMITY_LED_3			= bytearray(b'\x1B')
LED_DIGITS_0 			= bytearray(b'\x00')
ELIPSES_STRING			= bytearray(b'\x18')

############################# FUNCTION - DEFINITIONS ################################

#############################
# Helper Functions For Modes
#############################


def ok_button_pressed():
	if GPIO.input(11):
		time.sleep(0.5)
		return 1
	else:
		return 0


def up_button_pressed():
	if GPIO.input(10):
		time.sleep(0.5)
		return 1
	else:
		return 0


def down_button_pressed():
	if GPIO.input(14):
		time.sleep(0.5)
		return 1
	else:
		return 0


def left_button_pressed():
	if GPIO.input(18):
		time.sleep(0.5)
		return 1
	else:
		return 0


def right_button_pressed():
	if GPIO.input(4):
		time.sleep(0.5)
		return 1
	else:
		return 0


def generate_CHKSUM(command):
	for x in range(len(command)):
		if (x == 0):
			result = command[x]^command[x+1]
		elif(x >= 2):
			result = result^command[x]
	return result


def led_on(LED):
	command = bytearray(b'\x01\x13')
	command.extend(LED)
	command.extend(b'\x00\x01')
	CHKSUM = generate_CHKSUM(command)
	command.append(CHKSUM)
	ser.write(command)


def led_off(LED):
	command = bytearray(b'\x01\x13')
	command.extend(LED)
	command.extend(b'\x00\x00')
	CHKSUM = generate_CHKSUM(command)
	command.append(CHKSUM)
	ser.write(command)


# changing digits
# def change_dig(value):
# 	command = bytearray(b'\x01\x0F\x00')
# 	#insert value conversion
# 	CHKSUM = generate_CHKSUM(command)
# 	command.append(CHKSUM)
#  	ser.write(command)


# changing strings
def change_string(index, message):
	command = bytearray(b'\x02')
	command.extend(index)
	command.append(len(message))
	command.extend(message.encode("ascii"))
	command.append(generate_CHKSUM(command))
	ser.write(command)


def change_form(form): 			# Allows change of global variable "currentForm" without keyword
	global currentForm 
	currentForm = form
	command = bytearray(b'\x01\x0A')
	if(form == 1):
		command.extend(FORM_1_INDEX)								# add in binary, more than one 1, equals 0. otherwise 1
	elif(form == 2):
		command.extend(FORM_2_INDEX)
	elif(form == 3):
		command.extend(FORM_3_INDEX)
	elif(form == 4):
		command.extend(FORM_4_INDEX)
	elif(form == 5):
		command.extend(FORM_5_INDEX)
	elif(form == 6):
		command.extend(FORM_6_INDEX)
	elif(form == 7):
		command.extend(FORM_7_INDEX)
	command.extend(bytearray(b'\x00\x00'))
	CHKSUM = generate_CHKSUM(command)
	command.append(CHKSUM)
	ser.write(command)
	return None
	
#############################
# Selection Matrix Functions
#############################
def user_mode_select():
	mode = 0
	led_on(NETWORK_DETECT_LED)

	LED_DICT = {
		0: NETWORK_DETECT_LED,
		1: RF_DETECT_LED,
		2: FORM1_EXIT_LED
		}

	while(1):
		if(right_button_pressed() and (mode != 2)):
			led_off(LED_DICT[mode])
			mode += 1
			led_on(LED_DICT[mode])

		elif(left_button_pressed() and (mode != 0)):
			led_off(LED_DICT[mode])
			mode -= 1
			led_on(LED_DICT[mode])
		elif(ok_button_pressed()):
			break
	led_off(LED_DICT[mode])
	return mode

def network_select():
	mode = 0
	led_on(NETWORK_LED_0)

	NETWORK_DICT = {
		0: NETWORK_LED_0,
		1: NETWORK_LED_1,
		2: NETWORK_LED_2,
		3: NETWORK_LED_3,
		4: NETWORK_LED_4
		}

	# wifi scan code would go here

	ssid = []

	while(1):
		if(down_button_pressed() and (mode != 4)):
			led_off(NETWORK_DICT[mode])
			mode += 1
			led_on(NETWORK_DICT[mode])

		elif(up_button_pressed() and (mode != 0)):
			led_off(NETWORK_DICT[mode])
			mode -= 1
			led_on(NETWORK_DICT[mode])
		elif(ok_button_pressed()):
			break
	led_off(NETWORK_DICT[mode])
	return ssid


def keypad_selection():
	count = 0
	led_on(ENTER_KEY_LED)

	KEYPAD_LED_DICT = {
		0: ENTER_KEY_LED,
		1: KEYPAD_LED_0,
		2: KEYPAD_LED_1,
		3: KEYPAD_LED_2,
		4: KEYPAD_LED_3,
		5: KEYPAD_LED_4,
		6: KEYPAD_LED_5,
		7: KEYPAD_LED_6,
		8: KEYPAD_LED_7,
		9: KEYPAD_LED_8,
		10: KEYPAD_LED_9,
		11: KEYPAD_LED_10,
		12: KEYPAD_LED_11,

		13: KEYPAD_LED_0,
		14: KEYPAD_LED_1,
		15: KEYPAD_LED_2,
		16: KEYPAD_LED_3,
		17: KEYPAD_LED_4,
		18: KEYPAD_LED_5,
		19: KEYPAD_LED_6,
		20: KEYPAD_LED_7,
		21: KEYPAD_LED_8,
		22: KEYPAD_LED_9,
		23: KEYPAD_LED_10,
		24: KEYPAD_LED_11
		}

	keypad = {	1: '!@#$1', 2: 'abc2', 3: 'def3',
				4: 'ghi4',  5: 'jkl5', 6: 'mnop6',
				7: 'qrs7',  8: 'tuv8', 9: 'wxyz9',
				10:'shift', 11: '0 ' , 12: 'clear',

				13: '!@#$', 14: 'ABC2', 15: 'DEF3',
				16: 'GHI4', 17: 'JKL5', 18: 'MNOP6',
				19: 'QRS7', 20: 'TUV8', 21: 'WXYZ9',
				22: 'shift', 23: '0 ',   24: 'clear'
				}

	passcode = ""
	secrets = ""
	shift_val = 0

	while(1):
		if(ok_button_pressed() and (count == 10)):                 # lower ==> upper
			count += 12

		elif(ok_button_pressed() and (count == 22)):                # upper ==> lower
			count -= 12

		elif(ok_button_pressed() and (count == 12)):                # clear
			passcode = passcode[:-1]
			change_string(PASSWORD_STRING, passcode)

		elif(ok_button_pressed() and (count == 24)):                # clear
			passcode = passcode[:-1]
			change_string(PASSWORD_STRING, passcode)

		elif(ok_button_pressed() and (count != 0)):
			pad_string = keypad[count]
			passcode = passcode + pad_string[0]
			change_string(PASSWORD_STRING, passcode)

			change_char_index = 0

			t_end = time.time() + 6
			while(time.time() < t_end):
				if(ok_button_pressed()):
					if(change_char_index == (len(pad_string)-1)):
						change_char_index = 0
					else:
						change_char_index += 1
					passcode = passcode[:-1]
					passcode = passcode + pad_string[change_char_index]
					change_string(PASSWORD_STRING, passcode)

		elif(ok_button_pressed() and (count == 0)):
			return passcode

		elif(up_button_pressed() and (count not in [0,1,2,3,13,14,15])):
			led_off(KEYPAD_LED_DICT[count])
			count -= 3
			led_on(KEYPAD_LED_DICT[count])

		elif(down_button_pressed() and (count not in [0,10,11,12,22,23,24])):
			led_off(KEYPAD_LED_DICT[count])
			count += 3
			led_on(KEYPAD_LED_DICT[count])

		elif(left_button_pressed() and (count not in [0,1,4,7,10,13,16,19,22])):
			led_off(KEYPAD_LED_DICT[count])
			count -= 1
			led_on(KEYPAD_LED_DICT[count])

		elif(right_button_pressed() and (count not in [3,6,9,12,15,18,21,24])):
			led_off(KEYPAD_LED_DICT[count])
			count += 1
			led_on(KEYPAD_LED_DICT[count])

##############################
# Critical Functions For User
##############################


def boot_sequence():
	"""
		Anything that the NanoPi will need to initialize
		before proper function of the device
	"""
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)							# Sets numbering scheme for pin #'s
	GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin11 ok button     Initializes pin input and it's pullup/down
	GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin10 up button
	GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin14 down button
	GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin18 left button
	GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin22 right button
	GPIO.setup(9, GPIO.OUT)	 # pin9 ok button							                        Initializes pin output
	GPIO.setup(8, GPIO.OUT)	 # pin8	up button
	GPIO.setup(12, GPIO.OUT)  # pin12 down button						  set up which pins on the nano pi we will use
	GPIO.setup(16, GPIO.OUT)  # pin16 left button
	GPIO.setup(2, GPIO.OUT)	 # pin20 right button
	GPIO.output(9, GPIO.HIGH)							# Sets level of output pins; 3.3V or 0V
	GPIO.output(8, GPIO.HIGH)
	GPIO.output(12, GPIO.HIGH)
	GPIO.output(16, GPIO.HIGH)
	GPIO.output(2, GPIO.HIGH)


def network_scan():
	"""
		All network detection functionality using helper
		functions, user input, and serial talk to the display
	"""
	password = keypad_selection()

def rf_detect():
	"""
		This is where the GNU Radio code goes
		Should be copy paste, but will see about
		importing as class later
	"""

#################################### MAIN FUNCTION ##################################


print("This is the main function")
boot_sequence()

# Form 1
	# mode selection
# Form 2
	# select network
	# 5 labels, 5LEDs
# Form 3
	# enter network key
	# keypad, shift, clear
	# label as you enter keys
	# Okay LED to submit
# Form 4 - 6
	# mac address, possible device
	# 3 devices per form; 6 labels and 1 LED's per form
# Form 7
	# rf detection
	# 4 LEDs, 1 LED digits, 1 label for . . .

while(1):
	change_form(1)
	modeSelection = user_mode_select()
	if(modeSelection == 0):
		change_form(2)
		userNetwork = network_select()
		change_form(3)
		password = keypad_selection()
		network_scan(userNetwork, password)

	elif(modeSelection == 1):
		change_form(7)
		rf_detect()


	elif(modeSelection == 2):
		change_form(0)

	# exit sequence
