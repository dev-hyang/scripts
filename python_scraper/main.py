#!/usr/bin/python
import sys, getopt
from GenerateChristianBookTxt import *

def main(argv):
	prefix_url = ''
	pageIndex = ''
	bookname = ''
	try:
	  opts, args = getopt.getopt(argv,"hp:i:b:",["prefix_url=","pageIndex=", "bookname="])
	except getopt.GetoptError:
	  print('GenerateChristianBookTxt.py -p <prefix_url> -i <pageIndex> -b <bookname>')
	  sys.exit(2)
	for opt, arg in opts:
	  if opt == '-h':
	     print('GenerateChristianBookTxt.py -p <prefix_url> -i <pageIndex> -b <bookname>')
	     sys.exit()
	  elif opt in ("-p", "--prefix_url"):
	     prefix_url = arg
	  elif opt in ("-i", "--pageIndex"):
	     pageIndex = arg
	  elif opt in ("-b", "--bookname"):
	     bookname = arg
	print(prefix_url, pageIndex, bookname)
	
	bookWriter = GenerateChristianBookTxt(prefix_url, pageIndex, bookname)

	bookWriter.generateBook(prefix_url, pageIndex)

if __name__ == "__main__":
   main(sys.argv[1:])