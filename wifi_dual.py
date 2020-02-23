import os
import subprocess
import serial
import random
import time
import base64

bad_password_path = "bad_passwords.txt"

def main():
	ask()

def ask():
	username = input("username: ")
	#password = input("password: ")
	color = ''
	while color not in ["red", "blue"]:
		color = input("team color, red or blue? ")
		print(color)
		if color not in ["red", "blue"]:
			print("please choose either 'red' or 'blue' for your color")
	save_username(username)
	send_to_serial(find_device(), color)


def get_bad_password():
	with open(bad_password_path, "r") as f:
		 raw_bytes = f.readlines()[get_rand_from_seed(0, 49)].rstrip('\n')
		 return base64.b64decode(raw_bytes).decode('utf-8')

def find_device():
	result = subprocess.run(['find', '/dev', '-name', '*ttyUSB*'], stdout=subprocess.PIPE)
	serial_path = result.stdout.decode('utf-8').rstrip('\n')
	print(serial_path)
	return serial_path

def send_to_serial(serial_path, team_color):
	password = get_bad_password()
	print("ssid: {}\npassword: {}\nchannel: {}".format(team_color, password, get_rand_from_seed(1, 11)))
	output_string = 'ap -ssid "{}" -password "{}" -channel {}'.format(team_color, password, get_rand_from_seed(1, 11))
	print(output_string)
	ser = serial.Serial(serial_path, 115200)
	ser.write(output_string.encode())

def get_rand_from_seed(lower, upper):
	random.seed(time.time())
	return random.randint(lower, upper)

def save_username(username):
	filename = "usernames.txt"	
	if os.path.exists(filename):
	    append_write = 'a' # append if already exists
	else:
	    append_write = 'w' # make a new file if not
	with open(filename, append_write) as f:
		f.write(username)

main()

