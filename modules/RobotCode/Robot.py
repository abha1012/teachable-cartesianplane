#This is the class for the robot. It will be used to establish a connection 
#and send commands to the robot
#It supports forward, backward, turnLeft, turnRight
#It also supports forwardArrow, backwardArrow, which provide the ability to stop the robot using the arrow keys
#(if the robot is moving forward, the back key will stop it, and vice versa)

import serial
import threading
import sys

class Robot:
	#Overloads init method, establishes serial connection with robot
	def __init__(self):
		print ("Connecting to Robot")
		try:
			self._tty = serial.Serial(port="/dev/tty.TAG-DevB", baudrate=115200, timeout=0.01)
			self.forw = False
			self.back = False
			self.leftc = False
			self.rightc = False
			self.speed = 90
			self.turnSpeed = 55
			print ("Connected to Robot")
		except:
			print ("Could not Connect to Robot. Make sure the robot is on.")
			sys.exit()

	def setStraightSpeed(self, newSpeed):
		self.speed = newSpeed

	def setTurnSpeed(self, newSpeed):
		self.turnSpeed = newSpeed

	#utility function, returns the negative hex value
	def tohex(self, val, nbits):
  		return hex((val + (1 << nbits)) % (1 << nbits))

	#returns the hex value of the current speed to be sent to the robot
	def currentSpeed(self):
		return chr(self.speed)

	#returns the hex value of the current turn speed
	def currentTurnSpeed(self):
		return chr(self.turnSpeed)

	#returns the negative hex value of the current speed to be sent to the robot
	def currentNegSpeed(self):
		return chr((-self.speed + (1 << 8)) % (1 << 8))

	def currentNegTurnSpeed(self):
		return chr((-self.turnSpeed + (1 << 8)) % (1 << 8))

	def stop(self):
		self._tty.write(self.stopmotbSTR() + self.stopmotcSTR())
		forw = False
		back = False
		leftc = False
		rightc = False
    
	def stopmotbSTR(self):
	    return (chr(0x0C) + chr(0x00) + chr(0x80) + chr(0x04) + chr(0x01) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00))

	def stopmotcSTR(self):
	    return (chr(0x0C) + chr(0x00) + chr(0x80) + chr(0x04) + chr(0x02) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00))

	def forward(self):
	    self._tty.write(self.motbforwardSTR() + self.motcforwardSTR())
	    self.forw = True
	    self.back = False
	    self.rightc = False
	    self.leftc = False

	def beep(self):
	    self._tty.write(chr(0x06)+chr(0x00)+chr(0x80)+chr(0x03)+chr(0x0B)+chr(0x02)+chr(0xF4)+chr(0x01))

	#These are functions to turn on and off specific motors using the forwardSpeed(self.speed)
	def motbforwardSTR(self):
	    return (chr(0x0C) + chr(0x00) + chr(0x80) + chr(0x04) + chr(0x01) + self.currentSpeed() + chr(0x07) + chr(0x00) + chr(0x00) + chr(0x20) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00))
	    
	def motcforwardSTR(self):
	    return (chr(0x0C) + chr(0x00) + chr(0x80) + chr(0x04) + chr(0x02) + self.currentSpeed() + chr(0x07) + chr(0x00) + chr(0x00) + chr(0x20) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00))
	    
	def motbbackwardSTR(self):
	    return (chr(0x0C) + chr(0x00) + chr(0x80) + chr(0x04) + chr(0x01) + self.currentNegSpeed() + chr(0x07) + chr(0x00) + chr(0x00) + chr(0x20) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00))

	def motcbackwardSTR(self):
	    return (chr(0x0C) + chr(0x00) + chr(0x80) + chr(0x04) + chr(0x02) + self.currentNegSpeed() + chr(0x07) + chr(0x00) + chr(0x00) + chr(0x20) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00))

	#These are functions to turn on and off certain motors using the 
	def motbforwardTurn(self):
	    return (chr(0x0C) + chr(0x00) + chr(0x80) + chr(0x04) + chr(0x01) + self.currentTurnSpeed() + chr(0x07) + chr(0x00) + chr(0x00) + chr(0x20) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00))
	    
	def motcforwardTurn(self):
	    return (chr(0x0C) + chr(0x00) + chr(0x80) + chr(0x04) + chr(0x02) + self.currentTurnSpeed() + chr(0x07) + chr(0x00) + chr(0x00) + chr(0x20) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00))
	    
	def motbbackwardTurn(self):
	    return (chr(0x0C) + chr(0x00) + chr(0x80) + chr(0x04) + chr(0x01) + self.currentNegTurnSpeed() + chr(0x01) + chr(0x01) + chr(0x00) + chr(0x20) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00))

	def motcbackwardTurn(self):
	    return (chr(0x0C) + chr(0x00) + chr(0x80) + chr(0x04) + chr(0x02) + self.currentNegTurnSpeed() + chr(0x01) + chr(0x01) + chr(0x00) + chr(0x20) + chr(0x00) + chr(0x00) + chr(0x00) + chr(0x00))

	def turnRight(self):
	    self._tty.write(self.motcbackwardTurn() + self.motbforwardTurn())
	    self.forw = False
	    self.back = False
	    self.rightc = True
	    self.leftc = False

	def turnLeft(self):
	    self._tty.write(self.motbbackwardTurn() + self.motcforwardTurn())
	    self.forw = False
	    self.back = False
	    self.rightc = False
	    self.leftc = True
	    
	def backward(self):
	    self._tty.write(self.motbbackwardSTR() + self.motcbackwardSTR())
	    self.forw = False
	    self.back = True
	    self.rightc = False
	    self.leftc = False

	#This is a backwards command to be used with the arrow. If the robot is currently moving forward, the back button will
	#stop the robot. Otherwise, it will make it go backwards
	def backwardArrow(self):
		if self.forw:
			self.stop()
			self.forw = False
			self.backward()
		elif self.back:
			self.stop()
			self.back = False
		else:
			self.backward()

	#The reverse command from above
	def forwardArrow(self):
		if self.back:
			self.stop()
			self.back = False
			self.forward()
		elif self.forw:
			self.stop()
			self.forw = False
		else:
			self.forward()

	def leftArrow(self):
		if self.leftc:
			self.stop()
			self.leftc = False
		elif self.rightc:
			self.stop()
			self.rightc = False
			self.turnLeft()
		else:
			self.turnLeft()


	def rightArrow(self):
		if self.rightc:
			self.stop()
			self.rightc = False
		elif self.leftc:
			self.stop()
			self.leftc = False
			self.turnRight()
		else:
			self.turnRight()
		


