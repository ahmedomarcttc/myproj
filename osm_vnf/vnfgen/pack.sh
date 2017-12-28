#!/bin/bash

./generate_descriptor_pkg.sh -t vnfd -N http_vnfd
./generate_descriptor_pkg.sh -t vnfd -N l4fw_vnfd
./generate_descriptor_pkg.sh -t vnfd -N proxy_vnfd

./generate_descriptor_pkg.sh -t nsd -N demo_nsd
