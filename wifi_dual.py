import os
import subprocess
import serial
import random
import time
import base64
import pexpect

def main():
	get_user_input()


def get_user_input():
	username = input("username: ")
	color = ''
	while color not in ["red", "blue"]:
		color = input("team color, red or blue? ")
		print(color)
		if color not in ["red", "blue"]:
			print("please choose either 'red' or 'blue' for your color")
	password = get_bad_password()
	send_to_serial(find_device(), color, password)
	save_username(username, password)


def send_to_serial(serial_path, team_color, password):
	startAP_string = 'ap -ssid "{}" -password "{}" -channel {}'.format(team_color, password, get_rand_from_seed(1, 11))
	ser = serial.Serial(serial_path, 115200)
	ser.write(startAP_string.encode())
	print("access pont created")

	# change ssh password
	child = pexpect.spawn('passwd root')
	child.delaybeforesend = 2
	child.sendline(password)
	child.sendline(password)
	print("changed ssh password")


def get_bad_password():
	with open("bad_passwords.txt", "r") as f:
		 raw_bytes = f.readlines()[get_rand_from_seed(0, 49)].rstrip('\n')
		 return base64.b64decode(raw_bytes).decode('utf-8')


def find_device():
	result = subprocess.run(['find', '/dev', '-name', '*ttyUSB*'], stdout=subprocess.PIPE)
	serial_path = result.stdout.decode('utf-8').rstrip('\n')
	if len(serial_path) > 1:
		device_list = serial_path.splitlines()
		if len(device_list) == 1:
			return serial_path
		else:
			chosen = -1
			while chosen not in range(len(device_list)):
				print("multiple serial devices have been detected,\nplease choose one from the following list:")
				for n, device in enumerate(device_list):
					print("[ {} ] - {}".format(n+1, device))
				chosen = input("please type the number corresponding to the device you wish to connect to: ")
				chosen = int(chosen) - 1
				if chosen not in range(len(device_list)):
					print('incorrect device entered, try again...')
			return device_list[chosen]
	else:
		print('No serial device is connected, connect a serial device via USB and try again')
		time.sleep(3)
		exit()


def save_username(username, password):
	filename = "usernames_w_passwords.txt"	
	if os.path.exists(filename):
	    append_write = 'a' # append if already exists
	else:
	    append_write = 'w' # make a new file if not
	with open(filename, append_write) as f:
		password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
		line = "{}, {}\n".format(username, password)
		f.write(line)


def get_rand_from_seed(lower, upper):
	random.seed(time.time())
	return random.randint(lower, upper)


main()


