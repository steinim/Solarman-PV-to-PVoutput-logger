import datetime
import time
import urllib2
import urllib
import json
from StringIO import StringIO    
import sys
import httplib

pvo_host= "pvoutput.org"

pvo_key = "93f95e447f74a678b492b6c459030bc433c64d69"
pvo_systemid = "30465"                                  # Your PVoutput system ID here
pvo_statusInterval = 5                                  # Your PVoutput status interval - normally 5, 10 (default) or 15


apiDelay = 5 # time to delay after API calls

class Connection():
	def __init__(self, api_key, system_id, host):
		self.host = host
		self.api_key = api_key
		self.system_id = system_id

	def add_output(self, date, generated, exported=None, peak_power=None, peak_time=None, condition=None,
			min_temp=None, max_temp=None, comments=None, import_peak=None, import_offpeak=None, import_shoulder=None):
		"""
		Uploads end of day output information
		"""
		path = '/service/r1/addoutput.jsp'
		params = {
				'd': date,
				'g': generated
				}
		if exported:
			params['e'] = exported
		if peak_power:
			params['pp'] = peak_power
		if peak_time:
			params['pt'] = peak_time
		if condition:
			params['cd'] = condition
		if min_temp:
			params['tm'] = min_temp
		if max_temp:
			params['tx'] = max_temp
		if comments:
			params['cm'] = comments
		if import_peak:
			params['ip'] = import_peak
		if import_offpeak:
			params['op'] = import_offpeak
		if import_shoulder:
			params['is'] = import_shoulder

		response = self.make_request('POST', path, params)

		if response.status == 400:
			raise ValueError(response.read())
		if response.status != 200:
			raise StandardError(response.read())

	def add_status(self, date, time, energy_exp=None, power_exp=None, energy_imp=None, power_imp=None, temp=None, vdc=None, cumulative=False):
		"""
		Uploads live output data
		"""
		path = '/service/r2/addstatus.jsp'
		params = {
				'd': date,
				't': time
				}
		if energy_exp:
			params['v1'] = energy_exp
		if power_exp:
			params['v2'] = power_exp
		if energy_imp:
			params['v3'] = energy_imp
		if power_imp:
			params['v4'] = power_imp
		if temp:
			params['v5'] = temp
		if vdc:
			params['v6'] = vdc
		if cumulative:
			params['c1'] = 1
		params = urllib.urlencode(params)

		response = self.make_request('POST', path, params)

		if response.status == 400:
			raise ValueError(response.read())
		if response.status != 200:
			raise StandardError(response.read())

	def get_status(self, date=None, time=None):
		"""
		Retrieves status information
		"""
		path = '/service/r1/getstatus.jsp'
		params = {}
		if date:
			params['d'] = date
		if time:
			params['t'] = time
		params = urllib.urlencode(params)

		response = self.make_request("GET", path, params)

		if response.status == 400:
			raise ValueError(response.read())
		if response.status != 200:
			raise StandardError(response.read())

		return response.read()

	def delete_status(self, date, time):
		"""
		Removes an existing status
		"""
		path = '/service/r1/deletestatus.jsp'
		params = {
				'd': date,
				't': time
				}
		params = urllib.urlencode(params)

		response = self.make_request("POST", path, params)

		if response.status == 400:
			raise ValueError(response.read())
		if response.status != 200:
			raise StandardError(response.read())

		return response.read()

	def make_request(self, method, path, params=None):
		conn = httplib.HTTPConnection(self.host)
		headers = {
				'Content-type': 'application/x-www-form-urlencoded',
				'Accept': 'text/plain',
				'X-Pvoutput-Apikey': self.api_key,
				'X-Pvoutput-SystemId': self.system_id
				}
		conn.request(method, path, params, headers)

		return conn.getresponse()

pvoutz = Connection(pvo_key, pvo_systemid, pvo_host)

# show console output
powerdate = 20140928
powerTime = datetime.datetime.now().time()
PowerGeneration = 1234
Temperature = 23.4
Voltage = 210.7

print "Date: " + str(powerdate) + "Time: " + str(powerTime) + " W: " + str(PowerGeneration) + " temp: " + str(Temperature) + " volt: " + str(Voltage)

# update pvoutput
if(PowerGeneration): # make sure that we have actual values...
    pvoutz.add_status(powerdate, powerTime, power_exp=PowerGeneration, temp=str(Temperature), vdc=str(Voltage))
    print "Sucessful Log "
	#Ensure API limits adhered to
    time.sleep(apiDelay)
else:
	print "aint no data bitch.. make the sun come up"

print "Data Posted"
