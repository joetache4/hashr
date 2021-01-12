# hashr
Recursively scan a directory and compute hashes for all files.

Hash options include MD5, SHA1, SHA256, and SHA512.

# Usage
    hashr.py FILE_OR_ROOT_DIR [--md5 | --sha1 | --sha256 | --sha512] [--xf FILE [FILE ...]] [--xd DIR [DIR ...]]

## Positional Arguments
    FILE_OR_ROOT_DIR      specify the file or root directory for hashing

## Optional Arguments
    -h, --help            show this help message and exit
    --md5                 use MD5 algorithm (this is the default)
    --sha1                use SHA1 algorithm
    --sha256              use SHA256 algorithm
    --sha512              use SHA512 algorithm
    --xf FILE [FILE ...]  specify files not to hash (uses Unix-style wildcard matching)
    --xd DIR [DIR ...]    specify directories not to scan (uses Unix-style wildcard matching)