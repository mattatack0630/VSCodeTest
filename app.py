
from pyicloud import PyiCloudService
from time import sleep
from math import sqrt
import time

def auth_devices(api):
	import click

	print "Two-factor authentication required. Your trusted devices are:"

	devices = api.trusted_devices
	for i, device in enumerate(devices):
		print "  %s: %s" % (i, device.get('deviceName',
    		"SMS to %s" % device.get('phoneNumber')))

	device = click.prompt('Which device would you like to use?', default=0)
	device = devices[device]
	if not api.send_verification_code(device):
		print "Failed to send verification code"
		sys.exit(1)

	code = click.prompt('Please enter validation code')
	if not api.validate_verification_code(device, code):
		print "Failed to verify verification code"
		sys.exit(1)  

def email_location(loc):
	print("Emailing location")

def same_loc(loc_a, loc_b, max_dist):

	if(loc_a is None or loc_b is None):
		return False

	x_dist = (loc_a['latitude'] - loc_b['latitude'])
	y_dist = (loc_a['longitude'] - loc_b['longitude'])
	h_dist = sqrt((x_dist * x_dist) + (y_dist * y_dist))
	
	return h_dist < max_dist
	
api = PyiCloudService('mattatack0630@live.com', 'Mattman0630')

if api.requires_2fa:
	auth_devices()

update_rate = 10 #seconds
time_threshold = 60 #seconds
dist_threshold = 1
curr_location = None
last_location = None
sent_email = False

while(True):
	curr_location = api.devices[0].location()
	print "%f, %f" % (api.devices[0].location()['longitude'], api.devices[0].location()['latitude'])

	if same_loc(last_location, curr_location, dist_threshold) :
		elapsed_time = time.time() - then
	
		if(elapsed_time > time_threshold and not sent_email):
			email_location(curr_location)
			sent_email = True
	else:
		then = time.time()
		sent_email = False
		
	last_location = curr_location

	sleep(update_rate);