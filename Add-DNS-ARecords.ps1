﻿#Import CSV
$IPS = Import-CSV "C:\Users\ItIsMe\Downloads\IPList.csv"

foreach($IP in $IPS){

    Add-DnsServerResourceRecordA -ZoneName "test.local" -ComputerName "dnsserv.test.local" -Name $IP.name  -CreatePtr -IPv4Address $IP.ip

}