#Possible shebang would go here

#########
#Imports
#########
import serial as ser			#imports pySerial for comm with LCD
#import RPi.GPIO_NP as GPIO		#imports RPi.GPIO_NP to talk with GPIO pins
currentForm = 0					#global variable that should follow the current LCD screen form
										#Make sure to keep track of this value as it will change
										#between fucntions

############################# FUNCTION - DEFINITIONS ################################
def boot_sequence():
	"""
		Anything that the NanoPi will need to initialize
		before proper function of the device
	"""
	GPIO.setmode(GPIO.BOARD)
	pin_declarations()
	
def network_detect():
	"""
		All network detection functionality using helper
		functions, user input, and serial talk to the display
	"""
def rf_detect():
	"""
		This is where the GNU Radio code goes
		Should be copy paste, but will see about
		importing as class later
	"""
#############################
# Helper Functions For Modes
#############################
def user_mode_select():
	
#def led_on(index):
	
#def led_off(index):
	
def change_form(form): 			#Allows change of global variable "change_form" without keyword
	global currentForm 
	currentForm = form
	return None
	
def pin_declarations():
	GPIO.setup()
	
#################################### MAIN FUNCTION ##################################

def main():
	print("This is the main function")
	boot_sequence()
	
	while(1):
		if(currentForm == 0):
			user_mode_select()
			
		
if __name__ == "__main__":
	main()
