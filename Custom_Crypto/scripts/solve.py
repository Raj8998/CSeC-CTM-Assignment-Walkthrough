#!/usr/bin/python3
import re
from itertools import *
from base64 import b64decode

epitaph = b64decode(open("chocolate.txt", 'r').read()).decode()

# What we know: flag Format: CSeC{...} --> first 5 characters are known and last character is known.
# looking at the b64decoded text, we know first binary digits must be 1s as CS are there as it is, also there is a consecutive 4 characters so last binary value must also be 1, other than those we could guess but script should do our work.

clawList = list()
for claw in range(int(1e0), int(1e4)):
	binary = "".join(list(bin(claw)[-len(bin(claw))+2:len(bin(claw))]))
	if re.search('^11.*1$', binary) and binary.count('1') == 5:
		clawList.append(list(map(int, list(binary))))


length = 29
for claw in clawList:
	flag=[""]*29
	clawi=0
	flagi=0
	epitaphi=0
	wrongGuess = False
	while epitaphi<len(epitaph):
		if(claw[clawi%len(claw)] == 1):
			if(flag[flagi%29] == ""):
				flag[flagi%29] = epitaph[epitaphi]
			elif(flag[flagi%29] != "" and flag[flagi%29] != epitaph[epitaphi]):
				# print("Wrong Guess for claw ", claw)
				wrongGuess=True
				break;
			epitaphi=epitaphi+1
		flagi+=1
		clawi+=1
	if not wrongGuess:
		print("".join(flag), sep=": ")