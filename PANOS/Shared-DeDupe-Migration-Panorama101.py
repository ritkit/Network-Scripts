#!/usr/bin/env python3

# Shared-DeDupe-Migration-Panorama101.p
#
# Description
# This script will remove any duplicate items that match a shared
# policy object or security policy. It will also migrate items that 
# are duplicated across multiple firewalls. Only useful for Device
# Groups.
#
# Libraries
# Writer - Christian Rahl

import argparse
from curses import can_change_color
import requests
import yaml

parser = argparse.ArgumentParser(description="Run through Palo Alto Panorama to find
    duplicates across sites and merge them/punt them up to a shared policy")

parser.add_argument('-u', '--user', help='Provide username for accessing palo altos,
    without, user will be prompted, or yaml config checked')
parser.add_argument('-p', '--password' help='Provide the password, recommended is to
     exclude this flag as the user will be prompted in a more secure way. Yaml can
     be used also but also not recommended.')
parser.add_argument('-f', '--configfile', ,help='Yaml Config for modifying policies'
     required=True)

