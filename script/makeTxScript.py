import os
import random
import time
address_list = ["0x03710ff707a0e4dd3002dbf882957c865ffa1e65", \
		"0x7b4f9d90498a868b38b24e8259c2357290e6ba55", \
		"0x0b7ec4afd836c0f90820ba07bb661279dfa25576"]
SCRIPT_PATH="/home/jwpyo/etherbench/script.js"
PERIOD = 0.5

def makeScript(scriptpath):
	account1 = random.choice(address_list)
	account2 = random.choice(address_list)
	while account1 == account2:
		account2 = random.choice(address_list)
	with open(scriptpath, 'w') as f:
		tx = "var tx = {from: \"" + account1 + "\", to: \"" + account2 + "\", value: web3.toWei(0.02, \"ether\")};\n"
		command = "personal.sendTransaction(tx, \"a\");"
		for i in range(10000):
			f.write(tx)
			f.write(command)
def sendTransaction(scriptpath, period):
	while True:
		os.system("geth --exec 'loadScript(\""+scriptpath+"\")' attach /home/jwpyo/pidl_chain/geth.ipc")
		time.sleep(period)		

if __name__ == "__main__":
	makeScript(SCRIPT_PATH)
	sendTransaction(SCRIPT_PATH, PERIOD)
