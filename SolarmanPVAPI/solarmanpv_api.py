#!/usr/bin/env python
# -* coding: utf-8 *-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Developed 2016 by Christopher McAvaney <christopher.mcavaney@gmail.com>
# Intended for own use, but could be used by anybody who has a SolarmanPV Portal API key.
# Released to the public in 2016.

import requests
import datetime
from util import DEBUG
import sys

solarman_pv_api_base = 'https://openapi.solarmanpv.com/v1'

class SolarmanPVAPI:
	# NOTE: You will need to know the plant_id for the "plant" that you want to retrieve data
	def __init__(self, client_id, client_secret, plant_id):
		self.__client_id = client_id
		self.__client_secret = client_secret
		self.__plant_id = plant_id
		self.__access_token = ""
		self.__auth_headers = {}
		self.__authorised = False
		self.__requests_verify = True
		self.debug = True

		self.connected = self.__connect()

	def setDebug(self, debug):
		self.debug = debug

	def __str__(self):
		return self.__class__.__name__ + ' TO BE COMPLETED'

	def __connect(self):
		# Connect to the API and get the authorisation token required for subsequent requests
		url = solarman_pv_api_base + '/oauth2/accessToken?client_id=%s&client_secret=%s&grant_type=client_credentials' % (self.__client_id, self.__client_secret)
		try:
			response = requests.get(url, verify=self.__requests_verify)
		except requests.exceptions.RequestException as e:
			print '%s: connection failed - %s' % (self.__class__.__name__, e)
			return False

		# Grab the uid (which is just the client_id returned) and access_token and put them in a 
		# variable for subsequent API calls
		uid = response.json()['data']['uid']
		token = response.json()['data']['access_token']
		self.__auth_headers = {'uid':uid, 'token':token}

		self.__authorised = True
		return True

	# Allows sorting and deals with the case of no time value (shouldn't happen, but could do)
	def __extractTime(self, json):
		# Need to convert datetime to unixtime - even though value is UTC and this will change to localtime, 
		# not an issue as it is only for a relative comparison
		unix_ts = datetime.datetime.strptime(json['time'], "%Y-%m-%dT%H:%M:%SZ").strftime("%s")
		try:
			return int(unix_ts)
		except KeyError:
			return 0

	# Returns power data as a JSON object
	def getPower(self, date_to_retrieve=None, most_recent_value=None):
		if date_to_retrieve is None:
			date_to_retrieve = datetime.date.today().strftime('%Y-%m-%d')

		if self.debug:
			DEBUG('today == ' + date_to_retrieve)
			DEBUG('Getting plant power (for a day)')

		# Get the power data for a specified date or today
		url = solarman_pv_api_base + '/plant/power'
		params = {'plant_id':self.__plant_id, 'date':date_to_retrieve, 'timezone_id':'Australia/Canberra'}
		try:
			response = requests.get(url, verify=self.__requests_verify, headers=self.__auth_headers, params=params)
		except requests.exceptions.ConnectionError as e:
			print '%s: connection failed - %s' % (self.__class__.__name__, e)
			return None
			
		response.encoding = 'utf-8'

		if self.debug:
			print response
			print response.url
			print response.encoding
			print response.text
			#print response.json()

		# validate response
		if 'data' not in response.json() and 'powers' not in response.json():
			# should return None, maybe an exception
			print '%s: data or powers not in response: %s' % (self.__class__.__name__, response.text)
			return None

		if most_recent_value is True:
			# Sort the json() (just to be sure), take the last value
			power_data = response.json()['data']['powers']
			most_recent_power_data = None
			if isinstance(power_data, list): 
				power_data.sort(key=self.__extractTime, reverse=True)
				# temporary exception handler to nut out but first thing in the morning
				try:
					most_recent_power_data = power_data[0]
				except IndexError:
					# Some error in response from the API, i.e. an empty list
					most_recent_power_data = None
				except:
					# Effectively an unhandled error - retaining this debug whilst in beta testing mode
					print '%s: Exception: getPower(): An error with power_data %s' % (self.__class__.__name__, sys.exc_info()[0])
					print str(power_data)
					print power_data
			else:
				# temporary debug - whilst in beta testing mode
				print str(power_data)
			return most_recent_power_data
		else:
			return response.json()


# END OF FILE
