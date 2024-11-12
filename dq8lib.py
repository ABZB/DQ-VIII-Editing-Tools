from tkinter.filedialog import askopenfilename, asksaveasfilename
from os import SEEK_END

def bytes_to_write_little_endian(number, padding):
	temp = []
	
	while True:
		if(number == 0):
			for x in range(padding - len(temp)):
				temp.append(0)
			return(temp)
		
		temp.append(number & 0xFF)
		number = number >> 8
		
def get_file(target_name):
	source_file = []
	source_file_path = askopenfilename(title = 'Select ' + target_name)

	with open(source_file_path, "r+b") as f:
		f.seek(0, SEEK_END)
		file_end = f.tell()
		f.seek(0, 0)
		block = f.read(file_end)
		
	for ch in block:
		source_file.append(ch)
	return(source_file, source_file_path)


def write_file(source_file, source_file_path):
    
    
	with open(source_file_path, "w+b") as f:
		f.write(bytes(source_file))