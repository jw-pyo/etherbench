import os
import random
import time
import sys

address_list = [ 
"0x5d785e5029f7c58b0271743561c7abc313c958e5",
"0x54d4ef36171403b0704fcefd341bb4a7f67099a5",
"0xcc0b8d831e07b0b38509fc96aa767030802e0e16",
"0xadc952302ca3be16bff0407136e5a7467b63cdc3",
"0xbc1fd556ad698b10064b5eb098df27db7e286224",
"0x20dbc63d54be9c4f12f2c7b6bd8d6eb9fc29fcc1",
"0xf65891fac51a5bd75c3f51bf1f3fdc8e2ca35e85",
"0x8de535777aaf87b16c87330b3efb3b2cdb5bc1db",
"0xd8f9547b72fe488db6c84b4a85e1f0e4fd6cf1c0",
"0x3f43568539a91917da0a1e156cbeae947b6895ca",
"0x5da5c4419fbb2f54b602dd398d94bcb53a2babbb",
"0x3ad0fae560a03a21ca9e5c241d1a936a5818ec7f",
"0x0ab7a19c3518a29e1004e283c8253f1ce02483cc",
"0x9e59b47c1749d5e61726e83f0a8e9231be2a5e8b",
"0x2ab0514b18487b84357f933416ddc65e520f382a",
"0x748ce4540ef524fc73e34dfb3d52f1cd10682dbc"
]
SCRIPT_PATH="/home/jwpyo/etherbench/script.js"
PERIOD = 0.5

def makeScript(scriptpath):
	account1 = address_list[int(sys.argv[1])]
	account2 = address_list[int(sys.argv[2])]
	#while account1 == account2:
	#	account2 = random.choice(address_list)
	with open(scriptpath, 'w') as f:
		tx = "var tx = {from: \"" + account1 + "\", to: \"" + account2 + "\", value: web3.toWei(0.0002, \"ether\")};\n"
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
