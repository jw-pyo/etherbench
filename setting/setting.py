#
# Contact: wjddn1801@snu.ac.kr
#

import sys
import os
import time

IMAGE_NAME = "etherbench:1.0"
miner_number = 4
miner_rpcports= [i for i in range(8000, 8000+miner_number)]
miner_networkports= [i for i in range(40000, 40000+miner_number)]
client_rpcports = [i for i in range(9000, 9016)]
client_networkports = [i for i in range(41000, 41016)]


def stop_containers():
	for i in range(miner_number):
		os.system("docker stop miner_"+str(i))

def stop_n_del_containers():
	for i in range(miner_number):
		os.system("docker rm -f miner_"+str(i))

def check_ports_valid():
	for i in miner_rpcports:
		ret_string = os.popen("netstat -an | grep "+str(i)).read()
		if ret_string != "":
			assert False, "port %r is already assigned" % i
	for i in miner_networkports:
		ret_string = os.popen("netstat -an | grep "+str(i)).read()
		if ret_string != "":
			assert False, "port %r is already assigned" % i

def make_containers():
	i = 0 
	for miner_rpc, miner_network in zip(miner_rpcports, miner_networkports): 
		os.system("docker run -it -d --privileged --name miner_"+str(i)+" -p "+str(miner_rpc)+":"+str(miner_rpc)+ \
			  " -p "+str(miner_network)+":"+str(miner_network)+" "+IMAGE_NAME)
		i += 1

def auto_rearrange_valid_port():
	count = 0
	while True:
		count = 0 
		for index, i in enumerate(miner_rpcports):
			ret_string = os.popen("netstat -an | grep "+str(i)).read()
			if ret_string != "":
				count += 1
				miner_rpcports[index] = max(miner_rpcports) + 1
				miner_networkports[index] = max(miner_networkports) + 1
		
		for index, i in enumerate(miner_networkports):
			ret_string = os.popen("netstat -an | grep "+str(i)).read()
			if ret_string != "":
				count += 1
				miner_rpcports[index] = max(miner_rpcports) + 1
				miner_networkports[index] = max(miner_networkports) + 1
		if count == 0:
			break
	miner_rpcports.sort()
	miner_networkports.sort()
	print("rearranged port- miner_rpoport: "+str(miner_rpcports)+"\n miner_networkports: "+str(miner_networkports))			
	

def run_geths():
	i = 0
	for miner_rpc, miner_network in zip(miner_rpcports, miner_networkports): 
		geth_command = "geth --identity \"testchain\" --rpc --rpcport \"{}\" --rpccorsdomain \"*\"  \
				port \"{}\" --nodiscover --networkid 2018".format(miner_rpc, miner_network)
		to_docker_command = "docker exec -it -d miner_"+str(i)+" "
		os.system(to_docker_command + geth_command)
		i += 1

def make_enode_list():
	# make enode.txt in each containers
	for i in range(miner_number):
		to_docker_command = "docker exec -d miner_"+str(i)+" bash -c "
		geth_command = "\"geth --exec \"admin.nodeInfo.enode\" attach > /home/jwpyo/enode{}.txt\"".format(i)
		print(to_docker_command+geth_command)
		os.system(to_docker_command+geth_command)
	time.sleep(5) #give time to make enode file
	for i in range(miner_number):
		to_docker_command = "docker cp miner_"+str(i)+":/home/jwpyo/enode"+str(i)+".txt /home/jwpyo/etherbench/enode/"
		print(to_docker_command)
		os.system(to_docker_command)

		 	

def exit():
	sys.exit()

if __name__ == "__main__":
	func = [stop_containers, stop_n_del_containers, check_ports_valid, auto_rearrange_valid_port, make_containers, run_geths, make_enode_list, exit]
	while True:
		menu = raw_input("""
Choose the number of func to execute:
0. stop_containers
1. stop_n_del_containers
2. check_ports_valid
3. auto_rearrange_valid_port
4. make_containers
5. run_geths
6. make_enode_list
7. exit
"""
)
		func[int(menu)]()			     
