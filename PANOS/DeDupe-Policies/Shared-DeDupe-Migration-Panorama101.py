#!/usr/bin/env python3

# Shared-DeDupe-Migration-Panorama101.p
#
# Description
# This script will remove any duplicate items that match a shared
# policy object or security policy. It will also migrate items that 
# are duplicated across multiple firewalls. Only useful for Device
# Groups not templates.
#
# Libraries
# Writer - Christian Rahl

import argparse
import getpass
import yaml
import panos

# Process the yaml config file
# Requirements for the config file
#   Must have PANOS Device IP
#   Must have login information if not provided via args or CLI input
#   Must have Panos version as specified in API
#   Must have Query info, location, what list of device groups will be searched or 
#       compared
#   If destination is not shared but another devicegroup like datacenter, specify
#   If a specific policy is to be cleaned up specify
#   Specify if duplicate policies are to be renamed and taged or deleted

def yamlimport(configfile):
    

# Run through the config policies one at a time starting with the top level device
def searchconfig(query):

#
def findduplicates(query):

#
def takeAction(task, query):


### Start of Main Body

# Handle arguments passed from command line
parser = argparse.ArgumentParser(description="Run through Palo Alto Panorama to find
    duplicates across sites and merge them/punt them up to a shared policy")

parser.add_argument('-u', '--user', help='Provide username for accessing palo altos,'
    'without, user will be prompted, or yaml config checked')

parser.add_argument('-p', '--password' help='Provide the password, recommended is to'
    'exclude this flag as the user will be prompted in a more secure way. Yaml can'
    'be used also but also not recommended.')

parser.add_argument('-f', '--configfile', help='Yaml Config for modifying policies', 
    required=True)

args = parser.parse_args()

# Process the yaml config file and receive an object for processing.
config = yamlimport(args.configfile)

