#!/bin/bash

# Simple script to run the Python code with personal parameters
# replace the IDs and keys with yours below

/home/chrismc/src/SOLAR-INVERTER-SOLARMAN/Solarman-PV-to-PVoutput-logger/SolarmanPV-to-PVoutput.py \
	--smpv_client_id <your Solarman client ID> \
	--smpv_client_secret <your Solarman secret API key> \
	--smpv_plant_id <your Solarman plant ID> \
	--pvo_key <your PVOutput secret API key> \
	--pvo_system_id <your PVOutput system ID>

# END OF FILE
