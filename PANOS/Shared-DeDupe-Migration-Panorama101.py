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
import requests
import yaml

parser = argparse.ArgumentParser(description="Run through Palo Alto Panorama 
    to find duplicates across sites and merge them/punt them up to a shared policy")

parser.add_argument('-f', '--configfile', )
