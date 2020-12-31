from pathlib import Path
import hashlib
import sys

def md5(f):
	BLOCKSIZE = 65536 # multiple of 128
	hasher = hashlib.md5()
	with open(f, 'rb') as file:
		while buf := file.read(BLOCKSIZE):
			hasher.update(buf)
	return hasher.hexdigest()

if __name__ == "__main__":
	try:
		sys.argv[2]
		sys.exit("[ERROR] Too many arguments. \n(Hint: Surround filename with quotes if it contains whitespace.)")
	except IndexError:
		pass

	try:
		root = sys.argv[1]
	except IndexError:
		root = input("Enter root: ")
	root = Path(root)

	if not root.exists():
		sys.exit(f"[ERROR] Root does not exist: {str(root)}")

	if root.is_file():
		files = (root,)
	else:
		files = (p for p in Path(root).rglob("*") if p.is_file())

	for f in files:
		print(f"{md5(f)} {str(f)}")