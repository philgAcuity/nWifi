import ui
import socket
import speech
from time import sleep

UDP_IP = "10.0.1.255"
UDP_PORT = 5556
globalPacketID = 0
channelSelection = 'Bedroom'
#channelSelection = 'Kitchen Island'
#channelSelection = 'Kitchen Table'

channelDict = {	'Bedroom' : '115', 
								'Kitchen Island' : '57', 'Kitchen Table' : '6',
								'Fireplace' : '100',
								'Garage Outdoor' : '28',
								}
rooms = ['Bedroom', 
					'Kitchen Island', 
					'Kitchen Table',
					'Fireplace',
					'Garage Outdoor',]

def SendNlightUdp(udp_ip, udp_port, message):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	for x in range(3):
		sock.sendto(message, (udp_ip, udp_port))
		sleep(0.3)
		print 'sending packet'
	print 'yay'
	
def SendNlightOn(myInterface):
	viewSelector = myInterface.superview
	global channelSelection
	speech.say('You pressed On ' + channelSelection)
	channel = '{:02X}'.format(int(channelDict[channelSelection])-1)
	print channel
	temp = BuildNlightPacket(dest='FFFFFFFC',
														src='FFFFFFF2',
														subj='00',
														payload='010100'+channel,
														packetID=True)
	message = bytearray.fromhex(temp)
	SendNlightUdp(UDP_IP, UDP_PORT, message)
	
def SendNlightOff(myInterface):
	viewSelector = myInterface.superview
	global channelSelection
	speech.say('You pressed Off ' + channelSelection)
	channel = '{:02X}'.format(int(channelDict[channelSelection])-1)
	print channel
	temp = BuildNlightPacket(dest='FFFFFFFC',
														src='FFFFFFF2',
														subj='00',
														payload='010000'+channel,
														packetID=True)
	message = bytearray.fromhex(temp)
	SendNlightUdp(UDP_IP, UDP_PORT, message)
	
def BuildNlightPacket(dest='FFFFFFFC',
											src='FFFFFFF2',
											subj='00',
											payload='00',
											packetID=True):
	global globalPacketID
	if packetID == True:
		globalPacketID +=1
		if globalPacketID > 255:
			globalPacketID = 0
		payload += '{:02X}'.format(globalPacketID)
	packet = 'A5' + dest + src + '{:02X}'.format(13 + len(payload)/2) + subj + payload
	bytes = list(bytearray.fromhex(packet))
	d0 = bytes[0::2]
	d1 = bytes[1::2]
	checkH = 0
	for b in d0:
		checkH ^= b
	checkH = ~(checkH) & 0xFF
	checkH = '{:02X}'.format(checkH)
	checkL = 0
	for b in d1:
		checkL ^= b
	checkL = ~(checkL) & 0xFF
	checkL = '{:02X}'.format(checkL)
	packet += checkH + checkL
	print packet
	return packet
		
def ChangeRooms(myInterface):
	global channelSelection
	channelSelection = rooms[myInterface.selected_row]
	print channelSelection
	
		



v = ui.load_view()
v.present('sheet')
