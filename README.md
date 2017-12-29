# myproj
MyProj

1. Installed OSM R3 from binaries (first option in etsi.osm.org website) using the Nested containers.
Although the installation process is well documented, I am rewriting the process,

	a. In a fresh Ubuntu 16.04 (64-bit variant required) VM do the following for LXD configuration
		sudo apt-get update
		sudo apt-get install -y lxd
		newgrp lxd
	(initialize LXD)
		sudo lxd init
		 Name of the storage backend to use (dir or zfs) [default=dir]:
		 Would you like LXD to be available over the network (yes/no) [default=no]?
		 Do you want to configure the LXD bridge (yes/no) [default=yes]?
		  Do you want to setup an IPv4 subnet? Yes
		   Default values apply for next questions
		  Do you want to setup an IPv6 subnet? No
		 LXD has been successfully configured.
	(Set a fix value for the MTU)
		lxc list
		ip address show ens3
		ip address show lxdbr0
		sudo lxc profile device set default eth0 mtu 1446
	(For testing)
		lxc launch ubuntu:16.04 test
		lxc exec test bash
		root@test:~# apt-get update
		root@test:~# exit
		lxc stop test
		lxc delete test
	(Nested LXD Configuration)
	     Launch the Host Container
		lxc launch ubuntu:16.04 osmr3 -c security.privileged=true -c security.nesting=true
	     Resource Limits
		lxc config set osmr3 limits.cpu 4
		lxc config set osmr3 limits.memory 8GB
	     Configuring the Host Container
		lxc exec osmr3 bash
		sudo apt update
		sudo apt upgrade
	(initialize LXD)
		sudo lxd init
		 Do you want to configure a new storage pool (yes/no) [default=yes]?
		 Name of the new storage pool [default=default]:
		 Name of the storage backend to use (dir, btrfs, lvm, zfs) [default=zfs]: dir
		 Would you like LXD to be available over the network (yes/no) [default=no]?
		 Would you like stale cached images to be updated automatically (yes/no) [default=yes]?
		 Would you like to create a new network bridge (yes/no) [default=yes]?
		 What should the new bridge be called [default=lxdbr0]?
		 What IPv4 address should be used (CIDR subnet notation, “auto” or “none”) [default=auto]?
		 What IPv6 address should be used (CIDR subnet notation, “auto” or “none”) [default=auto]? none
		 LXD has been successfully configured.

	b. While in the osmr3 container do the following,
		wget https://osm-download.etsi.org/ftp/osm-3.0-three/install_osm.sh
		chmod +x install_osm.sh
		./install_osm.sh

		At the end of the installation you will see the OSM_HOSTNAME IP (in my case it is 10.173.200.238)

		OSM client installed
		You might be interested in adding the following OSM client env variables to your .bashrc file:
		     export OSM_HOSTNAME=10.173.200.238
		     export OSM_RO_HOSTNAME=10.173.200.240


	c. Accessing the OSM Launchpad,
		To access the OSM Launchpad we need to route traffic from the Host Machine to the Host Container. After running the "lxc list" command we have,

		testbed@framework:~$ lxc list
    +-------+---------+--------------------------------+------+------------+-----------+
    | NAME  |  STATE  |              IPV4              | IPV6 |    TYPE    | SNAPSHOTS |
    +-------+---------+--------------------------------+------+------------+-----------+
    | osmr3 | RUNNING | 10.173.200.1 (lxdbr0)          |      | PERSISTENT | 0         |
    |       |         | 10.160.50.193 (eth0)           |      |            |           |
    +-------+---------+--------------------------------+------+------------+-----------+
		Now we run the following command,
		testbed@framework:~$ sudo route add -net 10.173.200.0/24 gw 10.160.50.193

		d.  Now, Open a browser (Chrome in my case) and use the following URL,
			https://10.173.200.238:8443

2. The process of installing the VIM-EMU tool is very easy and it is also shown in the ETSI OSM website (https://osm.etsi.org/wikipub/index.php/VIM_emulator). However I have created a bash file which does the whole process with one command.

		a. Run the file "vimemu-install.sh" (which is myproj/scripts/) so,
			testbed@framework:~$ cd myproj/scripts/
			testbed@framework:~$ chmod +x vimemu-install.sh #when downloaded for the first time
			testbed@framework:~$ ./vimemu-install.sh

		b. Now we can run emulated Network topologies just like in mininet. In our case we run the file "demo_topo.py" to emulate a 2pop network.
			testbed@framework:~$ cd myproj/scripts/
			testbed@framework:~$ sudo python demo_topo.py
			.
			.
			containernet>

		c. To see the emulator dashboard we can use the following link in a browser,
		 	http://127.0.0.1:5001/dashboard/index_upb.html

3. It is time to get some VNFs and NSs running,

		a. Create and attach the POPs (which are emulated in topology) in the RO container
			export OPENMANO_TENANT=osm
			openmano tenant-create osm
			openmano datacenter-create pop1 http://172.31.255.1:6001/v2.0 --type openstack --description "osm-pop1"
			openmano datacenter-create pop2 http://172.31.255.1:6002/v2.0 --type openstack --description "osm-pop2"
			openmano datacenter-attach pop1 --user=username --password=password --vim-tenant-name=tenantName
			openmano datacenter-attach pop2 --user=username --password=password --vim-tenant-name=tenantName

		b. There are some example VNFs and NS in /myproj/osm_vnf/pkggen folder,
			testbed@framework:~$ cd myproj/osm_vnf/pkggen/
			testbed@framework:~/myproj/osm_vnf/pkggen$ ./pack.sh

		c. In the OSM Launchpad login using Username- admin Password- admin
			.
			.
			Rest coming soon!!!!
