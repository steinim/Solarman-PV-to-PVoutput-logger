#!/usr/bin/python
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

import datetime, calendar
import sys

# Auxiliary routine
def DEBUG(*s):
	out = [datetime.datetime.now().isoformat() + ':',] + [str(x) for x in s]
	# only output when run at the command line, not from a cron job or redirection, etc
	if sys.stdout.isatty():
		print(' ' . join(out))

def utc_to_local(utc_dt):
	# get integer timestamp to avoid precision lost
	timestamp = calendar.timegm(utc_dt.timetuple())
	local_dt = datetime.datetime.fromtimestamp(timestamp)
	assert utc_dt.resolution >= datetime.timedelta(microseconds=1)
	return local_dt.replace(microsecond=utc_dt.microsecond)

# END OF FILE
