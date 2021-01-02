'''
Recursively compute hashes for all files in a directory.

Hash options include MD5, SHA1, SHA256, and SHA512.

author: Joe Tacheron
'''

from pathlib import Path
from fnmatch import fnmatch
import argparse
import hashlib

class PathType(object):
	'''Used with argparse as a type indicating a file or directory.'''

	def __init__(self, exists=True, type='file', dash_ok=False):
		'''
		exists:
			True: a path that does exist
			False: a path that does not exist
			None: don't care
		type: file, dir, None, or a function returning True for a valid Path object
			None: don't care
		dash_ok: whether to allow '-' as stdin/stdout
		'''

		assert exists in (True, False, None)
		assert type in ('file', 'dir', None) or hasattr(type, '__call__')

		self._exists = exists
		self._type = type
		self._dash_ok = dash_ok

	def __call__(self, s):
		p = Path(s)
		if s == '-':
			# the special argument '-' means sys.std{in,out}
			if not self._dash_ok:
				raise argparse.ArgumentTypeError('standard input/output (-) not allowed')
			if self._type == 'dir':
				raise argparse.ArgumentTypeError('standard input/output (-) not allowed as directory path')
		
		else:
			# check existence
			e = p.exists()
			if self._exists == True:
				if not e:
					raise argparse.ArgumentTypeError(f'path does not exist: {s}')
			elif self._exists == False:
				if e:
					raise argparse.ArgumentTypeError(f'path exists: {s}')
			
			if e:
				# if it exists, check its type
				if self._type is None:
					pass
				elif self._type == 'file':
					if not p.is_file():
						raise argparse.ArgumentTypeError(f'path is not a file: {s}')
				elif self._type == 'dir':
					if not p.is_dir():
						raise argparse.ArgumentTypeError(f'path is not a directory: {s}')
				elif not self._type(p):
					raise argparse.ArgumentTypeError(f'path not valid: {s}')
			#else:
			#	# if it doesn't exist, check that the parent dir is valid
			#	parent = p.resolve().parent
			#	if not parent.is_dir():
			#		raise argparse.ArgumentTypeError(f'parent path is not a directory: '{parent}'')

		return p

def digest(f, hasher, blocksize):
	with open(f, 'rb') as file:
		while buf := file.read(blocksize):
			hasher.update(buf)
	return hasher.hexdigest()

md5    = lambda f: digest(f, hashlib.md5(),    128*512)
sha1   = lambda f: digest(f, hashlib.sha1(),   160*512)
sha256 = lambda f: digest(f, hashlib.sha256(), 256*512)
sha512 = lambda f: digest(f, hashlib.sha512(), 512*512)

def scan(path, hash, exclude_files, exclude_dirs):
	'''Recursively scan dir for files to hash.'''
	
	if path.is_file() and not any(fnmatch(path.name, pat) for pat in exclude_files):
		print(f'{hash(path)} {str(path)}')
	elif path.is_dir() and not any(fnmatch(path.name, pat) for pat in exclude_dirs):
		for p in path.iterdir():
			scan(p, hash, exclude_files, exclude_dirs)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('root', metavar='FILE_OR_ROOT_DIR', type=PathType(exists=True, type=None), help='specify the file or root directory for hashing')
	
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--md5', action='store_const', const=md5, dest='hash', help='use MD5 algorithm (this is the default)',)
	group.add_argument('--sha1', action='store_const', const=sha1, dest='hash', help='use SHA1 algorithm')
	group.add_argument('--sha256', action='store_const', const=sha256, dest='hash', help='use SHA256 algorithm')
	group.add_argument('--sha512', action='store_const', const=sha512, dest='hash', help='use SHA512 algorithm')
	parser.set_defaults(hash=md5)
	
	parser.add_argument('--xf', metavar='FILE', nargs='+', default=[], help='specify files not to hash (uses Unix-style wildcard matching)')
	parser.add_argument('--xd', metavar='DIR', nargs='+', default=[], help='specify directories not to scan (uses Unix-style wildcard matching)')
	
	args = parser.parse_args()
	scan(args.root, args.hash, args.xf, args.xd)
	#input('Done. Press Enter to exit.')