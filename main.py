"""
Usage:
  python main.py virus_scan img
  python main.py text_scan img
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
import cv2

from docopt import docopt

from PIL import Image
from pytesseract import pytesseract

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

def text_scan(directory):
  path_to_tesseract_executable = '/usr/local/bin/tesseract'
  # If tesseract isn't on the PATH, you can point to the executable like this:
  #pytesseract.tesseract_cmd = path_to_tesseract_executable
  # tesseract --print-parameters
  # brew info tesseract
  #  /usr/local/Cellar/tesseract/5.2.0
  # https://nanonets.com/blog/ocr-with-tesseract/
  # https://pyimagesearch.com/2021/11/15/tesseract-page-segmentation-modes-psms-explained-how-to-improve-your-ocr-accuracy/

  files = FS.walk(directory)
  for file in files:
    abspath = file['abspath']
    if is_image_file(abspath):
      start_ms = int(round(time.time() * 1000))
      #img = Image.open(abspath)

      # See https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
      img = cv2.imread(abspath)
      grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert the image to gray scale
      ret, thresh1 = cv2.threshold(grayImg, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
      rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
      dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
      contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
      for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        rect = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cropped = img[y:y + h, x:x + w]
        custom_config = r'-l eng'  # '-l eng --psm 6'
        text = pytesseract.image_to_string(cropped)  # (cropped, config=custom_config, timeout=5.0)
        print("text scan file: {}, text: '{}'".format(abspath, text))

      # custom_config = r'-l eng --psm 6'
      # text = pytesseract.image_to_string(grayImg, config=custom_config, timeout=2.0)
      # finish_ms = int(round(time.time() * 1000))
      # elapsed_ms = finish_ms - start_ms
      # print("text scan file: {}, size: {}, text: '{}', milliseconds: {}".format(
      #   abspath, grayImg.size, text, elapsed_ms))


def is_image_file(filename):
  if filename.endswith('.png'):
    return True 
  if filename.endswith('.jpeg'):
    return True 
  return False

if __name__ == "__main__":
  if len(sys.argv) > 1:
    func = sys.argv[1].lower()

    if func == 'virus_scan':
      directory = sys.argv[2]
      virus_scan(directory)

    elif func == 'text_scan':
      directory = sys.argv[2]
      text_scan(directory)

    else:
        print_options('Error: invalid function: {}'.format(func))
  else:
    print_options('Error: no command-line arguments')
