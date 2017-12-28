#!/bin/bash

#OSM client installed
#You might be interested in adding the following OSM client env variables to your .bashrc file:
#     export OSM_HOSTNAME=10.173.200.238
#     export OSM_RO_HOSTNAME=10.173.200.240

#Route traffic from the Host Machine(IP of eth0 of osmr3)
#to the Host Container (Network address of lxdbr0 of osmr3)
sudo route add -net 10.173.200.0/24 gw 10.160.50.193
