"""
Usage:
  python main.py virus_scan img
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "2022/08/12"

import base64
import json
import sys
import time
import os

import arrow 
import clamd

from docopt import docopt

from pysrc.env import Env
from pysrc.fs import FS

def print_options(msg):
  print(msg)
  arguments = docopt(__doc__, version=__version__)
  print(arguments)

def virus_scan(directory):
  # See https://pypi.org/project/clamd/

  local_socket = '/tmp/clamd.socket'  # See line 96 of clamd.conf: LocalSocket /tmp/clamd.socket
  print('virus_scan, directory:  {}'.format(directory))
  print('connecting to clamd at: {}'.format(local_socket))

  # Connect to the clamd daemon, ping it, display its' version
  cd = clamd.ClamdUnixSocket(local_socket)    
  cd.ping()
  print('clamd version: {}'.format(cd.version()))

  files = FS.walk(directory)
  for file in files:
    abspath = file['abspath']
    start_ms = int(round(time.time() * 1000))
    result = cd.scan(abspath)
    finish_ms = int(round(time.time() * 1000))
    elapsed_ms = finish_ms - start_ms
    print('virus scan result: {}, milliseconds: {}'.format(result, elapsed_ms))


if __name__ == "__main__":
  if len(sys.argv) > 1:
    func = sys.argv[1].lower()
    print('func: {}'.format(func))

    if func == 'virus_scan':
      directory = sys.argv[2]
      virus_scan(directory)

    elif func == 'xxx':
      xxx()

    else:
        print_options('Error: invalid function: {}'.format(func))
  else:
    print_options('Error: no command-line arguments')
