# Working only with registers $s e $t, with functions add, addi, lw, sw, j, beq
# Small memory has been used for demonstration

import numpy as np

instructions = ['add', 'addi', 'lw', 'sw', 'j', 'beq']

file = open('example.txt', 'r')
mipsText = file.readlines()
file.close()
mipsText = [i.replace('\n', '').replace('\t', '').replace(',', '').replace(':', '').split() for i in mipsText]
labels = [ i[0] if i[0] not in instructions else '' for i in mipsText]
mipsText = [ mipsText[i] if labels[i]=='' else mipsText[i][1:] for i in range(len(labels))]

PC = 0
	
registers = np.zeros((32, 1))
#T => 8 - 15
#S => 16 - 23

memory = np.zeros((32, 1))

def encode(textFile): 
	for line in range(len(textFile)):
		if len(textFile[line]) == 0:
			pass
		elif textFile[line][0] == 'add':
			code1 = int(textFile[line][1][-1])+8 if (textFile[line][1].startswith('$t')) else int(textFile[line][1][-1])+16
			code2 = int(textFile[line][2][-1])+8 if (textFile[line][2].startswith('$t')) else int(textFile[line][2][-1])+16
			code3 = int(textFile[line][3][-1])+8 if (textFile[line][3].startswith('$t')) else int(textFile[line][3][-1])+16
			textFile[line] = [0, code1, code2, code3]

		elif textFile[line][0] == 'addi':
			code1 = int(textFile[line][1][-1])+8 if (textFile[line][1].startswith('$t')) else int(textFile[line][1][-1])+16
			code2 = int(textFile[line][2][-1])+8 if (textFile[line][2].startswith('$t')) else int(textFile[line][2][-1])+16
			code3 = int(textFile[line][3])
			textFile[line] = [1, code1, code2, code3]

		elif textFile[line][0] == 'lw' or textFile[line][0] == 'sw':
			code1 = int(textFile[line][1][-1])+8 if (textFile[line][1].startswith('$t')) else int(textFile[line][1][-1])+16
			code2 = int(textFile[line][2][:textFile[line][2].index('(')])
			code3 = int(textFile[line][2][textFile[line][2].index('t')+1:-1])+8 if (textFile[line][2][textFile[line][2].index('(')+1:].startswith('$t')) else int(textFile[line][2][textFile[line][2].index('s')+1:-1])+16
			textFile[line] = [2 if textFile[line][0] == 'lw' else 3, code1, code2, code3]

		elif textFile[line][0] == 'j':
			textFile[line] = [4, labels.index(textFile[line][1])]

		elif textFile[line][0] == 'beq':
			code1 = int(textFile[line][1][-1])+8 if (textFile[line][1].startswith('$t')) else int(textFile[line][1][-1])+16
			code2 = int(textFile[line][2][-1])+8 if (textFile[line][2].startswith('$t')) else int(textFile[line][2][-1])+16
			code3 = labels.index(textFile[line][3])
			textFile[line] = [5, code1, code2, code3]

	return textFile

def decisionOp(code):
	if len(code) == 0:
		pass
	elif code[0] == 0:
		add(code[1], code[2], code[3])
	elif code[0] == 1:
		addi(code[1], code[2], code[3])
	elif code[0] == 2:
		lw(code[1], code[2], code[3])
	elif code[0] == 3:
		sw(code[1], code[2], code[3])
	elif code[0] == 4:
		j(code[1])
	elif code[0] == 5:
		beq(code[1], code[2], code[3])
	

def add(writeRegister, register1, register2):
	registers[writeRegister] = registers[register1] + registers[register2]

def addi(writeRegister, register, immediate): 
	registers[writeRegister] = registers[register] + immediate

def lw(writeRegister, offSet, baseAddress): 
	address = (offSet/4) + registers[baseAddress]
	while address > len(memory)-1: address -= len(memory)
	registers[writeRegister] = memory[int(address)]

def sw(readRegister, offSet, baseAddress):
	address = (offSet/4) + registers[baseAddress]
	while address > len(memory)-1: address -= len(memory)
	memory[int(address)] = registers[readRegister]

def j(numLabel):
	global PC
	PC = numLabel - 1

def beq(register1, register2, numLabel):
	global PC
	if registers[register1] == registers[register2]:
		PC = numLabel - 1

mipsCode = encode(mipsText.copy())

while (PC != len(mipsCode)):
	print('Executando a instrução {}'.format(' '.join(mipsText[PC])))
	decisionOp(mipsCode[PC])
	print('Registers:            Memory:')
	for i in range(len(registers)):
		if i > 7 and i < 16:
			print('$t{}: {}                  m{}: {}'.format(i-8, registers[i][0], i, memory[i][0]))
		elif i > 15 and i < 24:
			print('$s{}: {}                  m{}: {}'.format(i-16, registers[i][0], i, memory[i][0]))
		else:
			print('                        m{}: {}'.format(i, memory[i][0]))

	print("Press enter to contine")
	input()

	PC += 1;