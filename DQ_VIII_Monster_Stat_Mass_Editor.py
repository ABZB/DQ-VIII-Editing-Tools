from cmath import e
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

def bytes_to_write_little_endian(number, padding):
	temp = []
	
	while True:
		if(number == 0):
			for x in range(padding - len(temp)):
				temp.append(0)
			return(temp)
		
		temp.append(number & 0xFF)
		number = number >> 8

def stat_alter(source_data, target_stat, alter_mode, alter_number, regular_bool, boss_bool, memory_bool):
    
	
	cursor_offset = 0xF8
	
	byte_count = 0x2
	read_mode = ''
	
	

	#0x001 to 0x130 is regular
	#0x192 to 1F2 is boss (191 and 192 are the start-of-game Slimes, but that seems cruel)
	#0x1F3 to 214 is Memory
	#0x258 to 2BB, plus 384-387 are recruitable monsters
	#0x320 to 369 are monster arena enemies

	index_list = []

	if(regular_bool):
		index_list = [*index_list, *list(range(0x001, 0x130 + 1))]
	if(boss_bool):
		index_list = [*index_list, *list(range(0x192, 0x1F2 + 1))]
	if(memory_bool):
		index_list = [*index_list, *list(range(0x1F3, 0x214 + 1))]
	
		


	match target_stat:
		case "HP":
			cursor_offset += 0x0
			byte_count = 0x2
			read_mode = 'number'
		case "MP":
			cursor_offset += 0x2
			byte_count = 0x2
			read_mode = 'number'
		case "ATK":
			cursor_offset += 0x4
			byte_count = 0x2
			read_mode = 'number'
		case "DEF":
			cursor_offset += 0x6
			byte_count = 0x2
			read_mode = 'number'
		case "AGI":
			cursor_offset += 0x8
			byte_count = 0x2
			read_mode = 'number'
		case "WIS":
			cursor_offset += 0xA
			byte_count = 0x2
			read_mode = 'number'
		case "EXP":
			cursor_offset += 0xC
			byte_count = 0x4
			read_mode = 'number'
		case "GOLD":
			cursor_offset += 0x10
			byte_count = 0x4
			read_mode = 'number'
		case "Common Drop":
			cursor_offset += 0x14
			byte_count = 0x2
		case "Rare Drop":
			cursor_offset += 0x16
			byte_count = 0x2
		case "3 unk bytes":
			cursor_offset += 0x18
			byte_count = 0x3
		case "Resistances":
			cursor_offset += 0x1B
			byte_count = 0x10
			read_mode = 'bytefield'
		case "5 unk bytes":
			cursor_offset += 0x2B
			byte_count = 0x5
		case "Actions":
			cursor_offset += 0x30
			byte_count = 0x0C

	max_number = 0
	if(byte_count == 0x2):
		max_number = 0xFFFF
	elif(byte_count == 0x4):
		max_number = 0x7FFFFFFF



	for monster_index in index_list:
		#grab the appropriate bytes
		major_offset = (monster_index - 1) * 0xE0
		
		if(read_mode == 'number'):
			temp = 0
			
			for offset in range(byte_count):
				
				temp += source_data[major_offset + cursor_offset + offset]<<(offset*8)				
			if(temp == 0):
				pass
			
			match alter_mode:
				case '+':
					temp += alter_number
				case '*':
					temp *= alter_number
				case 'set':
					temp = alter_number
				case 'set min':
					temp = max(alter_number, temp)
				case 'set max':
					temp = min(alter_number, temp)
			
			temp = max(0,min(int(temp), max_number))
			temparry = bytes_to_write_little_endian(temp, byte_count)
			
			for offset in range(byte_count):
				source_data[major_offset + cursor_offset + offset] = temparry[offset]

		elif(read_mode == 'bytefield'):
			
			temp = []
			check = 0
			for offset in range(byte_count):
				temp.append(source_data[major_offset + cursor_offset + offset])
				check += temp[offset]
			
			if(check == 0):
				pass
			
			match alter_mode:
				case '+':
					for x in temp:
						x += alter_number
				case '*':
					for x in temp:
						x *= alter_number
				case 'set':
					for x in temp:
						x = alter_number
				case 'set min':
					for x in temp:
						x = max(alter_number, x)
				case 'set max':
					for x in temp:
						x = min(alter_number, x)
				
			for offset in range(byte_count):
				source_data[major_offset + cursor_offset + offset] = max(0,min(int(temp[offset]), 3))
	

	print('Completed applying ' + target_stat + ' ' + alter_mode + ' ' + str(alter_number))
	return(source_data)


def get_file():
	source_file = []
	source_file_path = askopenfilename(title = 'Select monster.tbl file')

	with open(source_file_path, "r+b") as f:
		f.seek(0, os.SEEK_END)
		file_end = f.tell()
		f.seek(0, 0)
		block = f.read(file_end)
		
	for ch in block:
		source_file.append(ch)
	return(source_file, source_file_path)


def write_file(source_file, source_file_path):
    
    
	with open(source_file_path, "w+b") as f:
		f.write(bytes(source_file))
	


def receive_input(source_data):
	
	
	outstring = ''
	regular_bool = False
	boss_bool = False
	memory_bool = False
	
	target_stat = ''

	alter_mode = ''
	
	alter_number = 0.0
	

	while True:
		while True:
			boolsetright = 'n'
			try:
				print('\n\nWhich blocks of monsters do you want to modify?\n')
				bool_set = input('Type any combination of R for regular, B for boss, and M for Memory Lane bosses\n')
			
				if('r' in bool_set.lower()):
					regular_bool = True
					outstring += 'Regular/'
				else:
					regular_bool = False	
				
				if('b' in bool_set.lower()):
					boss_bool= True
					outstring += 'Bosses/'
				else:
					boss_bool = False	
				
				if('m' in bool_set.lower()):
					memory_bool = True
					outstring += 'Memories'
				else:
					memory_bool = False
				

				if(not(regular_bool or boss_bool or memory_bool)):
					print('Invalid selection: ' + bool_set)
				else:
					break
				if(boolsetright == 'y'):
					break
			except Exception as e:
				print(e)
			

		while True:
			try:
				print('\nWhat value would you like to alter?')
				target_stat = input('HP, MP, Atk, Def, Agi, Wis, Exp, Gold\n')
			
				if(target_stat.upper() in {'HP', 'MP', 'ATK', 'DEF', 'AGI', 'WIS', 'EXP', 'GOLD'}):
					target_stat = target_stat.upper()
					break
				else:
					print('Invalid selection: ' + target_stat)
			except Exception as e:
				print(e)
			
		while True:
			try:
				print('\nWhat operation would you like to use?\n')
				alter_mode = input('+, *, set, set min, set max\n')
			
				if(alter_mode.lower() in {'+', '*', 'set', 'set min', 'set max'}):
					alter_mode = alter_mode.lower()
					break
				else:
					print('Invalid selection: ' + alter_mode)
			except Exception as e:
				print(e)
			
		while True:
			try:
				alter_number = input('\nBy what value?\n')
			
				if(isinstance(float(alter_number), float)):
					alter_number = float(alter_number)
					break
				else:
					print('Invalid selection: ' + alter_number)
			except Exception as e:
				print(e)
		
		while True:
			print('Modifying as follows:\n')
			print(outstring + ' ' + target_stat + ' ' + alter_mode + ' ' + str(alter_number))
			set_to_go = input('Is this correct? Y/N\n')
			if(set_to_go.lower() == 'y'):
				print('Modifying data')
				source_data = stat_alter(source_data, target_stat, alter_mode, alter_number, regular_bool, boss_bool, memory_bool)
				break
			else:
				restart = input('Do you want to choose a different selection? Y/N\n')
				if(restart.lower() == 'y'):
					break
				else:
					print('\n\n\n')
					
		while True:
			restart = input('Do you wish to modify anything else (note that saving the edited file will happen only after you say no)? Y/N\n')
			if(restart.lower() == 'y'):
				break
			else:
				return(source_data)
			
			

def main():
	

	while True:
		try:
			source_data, source_file_path = get_file()
			break
		except Exception as e:
			print(e)
	

	
	print('Saving .bak as backup')
	write_file(source_data, source_file_path + '.bak')
	
	source_data = receive_input(source_data)
	
	print('Saving edited file')
	write_file(source_data, source_file_path)
	

main()