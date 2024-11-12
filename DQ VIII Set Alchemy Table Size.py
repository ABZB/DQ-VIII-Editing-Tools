from dq8lib import *


#locations in code.bin where the table size is used
addresses_to_change = {0xec274, 0xec3b8, 0xec3fc, 0xec480, 0xec4b0, 0xec56c, 0xec5e4, 0xec65c, 0x12b084, 0x12b0a8, 0x12b4e8, 0x12b514, 0x12b66c, 0x12b6d0, 0x12bc38, 0x12bc60, 0x12bc80, 0x16425c, 0x1642bc, 0x1642e0, 0x1658d8, 0x1659b4, 0x165a5c, 0x1948bc, 0x1948c4, 0x1b227c, 0x2f2960, 0x2f3ae8, 0x2f4610, 0x39faa4}


def main():


	while True:
		try:
			source_data, source_file_path = get_file('code.bin')
			break
		except Exception as e:
			print(e)

	while True:
		try:
			table_size = input('Enter new table size\n')
			base_mode = input('Confirm base (d = decimal, h = hex)\n').lower()
			
			if(base_mode == 'd'):
				table_size = int(table_size, base = 10)
				break
			elif(base_mode == 'h'):
				table_size = int(table_size, base = 16)
				break
		except Exception as e:
			print(e)

	
	print('Saving backup\n')
	write_file(source_data, source_file_path + '.bak')
	
	for offset in addresses_to_change:
		source_data[offset] = table_size

	print('Saving edited file')
	write_file(source_data, source_file_path)
	

main()
