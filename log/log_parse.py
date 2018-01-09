import re
import os
import sys

def parse(filename):
	with open(filename, 'r') as f:
		contents = f.read()
		parse_file = open("parse_"+filename, 'w')
		for line in contents.split("\n"):
			time = re.compile(r'\d\d[:]\d\d[:]\d\d').search(line)
			commit = re.compile(r'Commit new mining work').search(line)
			imported = re.compile(r'Imported new chain segment').search(line)
			tx = re.compile(r'txs=\d+').search(line)
			num = re.compile(r'number=\d+').search(line)
			if time is not None and tx is not None and num is not None:
				if imported is not None:
					parse_file.write(time.group()+str(" ")+imported.group()+str(" ")+num.group()+str(" ")+tx.group()+str("\n"))
				elif commit is not None:
					parse_file.write(time.group()+str(" ")+commit.group()+str(" ")+num.group()+str(" ")+tx.group()+str("\n"))
				else:
					pass
		parse_file.close()


if __name__=="__main__":
	#parse("client16_miner_change.log")
	parse("miner8_client_change.log")
	
