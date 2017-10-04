import os
import re
import sys

def main(folder_path="."):
	for filename in os.listdir(folder_path):
		if filename.endswith(".pdf"):
			rm_ebook = re.sub(r'\s*\[e\w+\]\s*', '', filename, flags=re.I).strip(' ')
			rm_start_numbers = re.sub(r'^\d+-', '', rm_ebook, flags=re.I)
			new_name = rm_start_numbers[:-4].replace('_', ' ').title() + ".pdf"
			print("Viejo Nombre:", filename, "\nNuevo:", new_name,"\n")
			os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))


if __name__ == '__main__':
	if len(sys.argv) > 2:
		print("ERROR: Solo se puede un folder_pathumento", file=sys.stderr)
		sys.exit(-1)
	elif len(sys.argv) == 2:
		print("Trabajando en:", sys.argv[1])
		main(sys.argv[1])
	else:
		main()