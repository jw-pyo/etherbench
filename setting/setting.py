#
# Contact: wjddn1801@snu.ac.kr
#

import sys
import os
import time

IMAGE_NAME = "etherbench:1.1"
miner_number = int(sys.argv[1])
miner_rpcports= [i for i in range(8600, 8600+miner_number)]
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
	
def init_geths():
	i = 0
	for miner_rpc, miner_network in zip(miner_rpcports, miner_networkports): 
		to_docker_command = "docker cp /home/jwpyo/etherbench/genesis/custom_genesis.json miner_"+str(i)+":/home/jwpyo/"
		os.system(to_docker_command)
		print(to_docker_command)
		i += 1
	time.sleep(5)
		
	i = 0
	for miner_rpc, miner_network in zip(miner_rpcports, miner_networkports): 
		geth_command = "\"geth --datadir /home/jwpyo/pidl_chain init /home/jwpyo/custom_genesis.json\""
		to_docker_command = "docker exec -d miner_"+str(i)+" bash -c "
		os.system(to_docker_command + geth_command)
		print(to_docker_command + geth_command)
		i += 1
	
def run_geths():
	
	i = 0
	#1. make python script to execute geth and copy to each container
	for miner_rpc, miner_network in zip(miner_rpcports, miner_networkports):
		import_command = "import os\n" 
		geth_command = "os.system(\"geth --datadir /home/jwpyo/pidl_chain/ --networkid 19940512 --rpc --rpcport {} --port {} --nodiscover 2>> /home/jwpyo/gethinfo.log\")".format(miner_rpc, miner_network)
		with open("miner_exe/miner_"+str(i)+"_exe.py", "w") as f:
			f.write(import_command+geth_command)
		time.sleep(2)	
		docker_command = "docker cp miner_exe/miner_{}_exe.py miner_{}:/home/jwpyo/".format(i, i)
		os.system(docker_command)
		i += 1
	time.sleep(3) #give time about copy time
	i = 0
	#2. execute python script in each container
	for miner_rpc, miner_network in zip(miner_rpcports, miner_networkports): 
		docker_command = "docker exec -d miner_{} bash -c \"python /home/jwpyo/miner_{}_exe.py\"".format(i, i)
		os.system(docker_command)
		i += 1

def make_enode_list():
	# make enode.txt in each containers
	js_command = "console.log(admin.nodeInfo.enode);"
	with open("enode.js", "w") as f:
		f.write(js_command)
	time.sleep(2)	
	for i, (miner_rpc, miner_network) in enumerate(zip(miner_rpcports, miner_networkports)):
		docker_command = "docker cp enode.js miner_{}:/home/jwpyo/".format(i)
		os.system(docker_command)
	time.sleep(3) #give time about copy time
	
	for i in range(miner_number):
		to_docker_command = "docker exec -d miner_"+str(i)+" bash -c "
	#	geth_command = "\"geth --exec 'loadScript(\"/home/jwpyo/enode.js\")' attach /home/jwpyo/pidl_chain/geth.ipc > /home/jwpyo/enode{}.txt\"".format(i)
		geth_command = "\"geth --exec \"admin.nodeInfo.enode\" attach \"/home/jwpyo/pidl_chain/geth.ipc\" > /home/jwpyo/enode{}.txt\"".format(i)
		print(to_docker_command+geth_command)
		os.system(to_docker_command+geth_command)
	time.sleep(5) #give time to make enode file
	for i in range(miner_number):
		to_docker_command = "docker cp miner_"+str(i)+":/home/jwpyo/enode"+str(i)+".txt /home/jwpyo/etherbench/enode/"
		print(to_docker_command)
		os.system(to_docker_command)
#def trim_enodes():
	enode_file = open("enodes.txt", "w")
	for i, filename in enumerate(os.listdir("../enode/")):
		f = open("../enode/"+filename, 'r')
		sentence = "admin.addPeer("+str(f.read().strip())+")"
		sentence = sentence.replace("[::]", "172.17.0.{}".format(i+3))
		sentence = sentence.replace("?discport=0", "")
		enode_file.write(sentence)
		f.close()
		print(sentence)
		if i < miner_number - 1 : enode_file.write("\n")
	enode_file.close()

def addPeers(): #not working
	for i in range(miner_number):	
		enode = open("enodes.txt", "r")
		for ii, addpeer in enumerate(enode.read().split("\n")):
			command = "docker exec -d miner_{}".format(i)+ " bash -c " + "\"geth --exec " + addpeer + " attach /home/jwpyo/pidl_chain/geth.ipc\""
			if i != ii:
				print(command)
				#os.system(command)
		print("\n")
		enode.close()
	
def justPrintAddPeer():
	for i in range(miner_number):	
		enode = open("enodes.txt", "r")
		for ii, addpeer in enumerate(enode.read().split("\n")):
			if i != ii:
				print(addpeer)
		print("\n")
		enode.close()
		
		
		
		
		 	

def exit():
	sys.exit()

if __name__ == "__main__":
	func = [stop_containers, stop_n_del_containers, check_ports_valid, auto_rearrange_valid_port, make_containers, init_geths, run_geths, make_enode_list, addPeers, justPrintAddPeer, exit]
	while True:
		menu = raw_input("""
Choose the number of func to execute:
0. stop_containers
1. stop_n_del_containers
2. check_ports_valid
3. auto_rearrange_valid_port
4. make_containers
5. init_geths
6. run_geths
7. make_enode_list
8. addPeers
9. justPrintAddPeer
10. exit
Press the number:  
"""
)
		func[int(menu)]()			     
