import tornado.ioloop
import tornado.web
import io
import pybase64
from PIL import Image
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
import qrcode
import zbarlight
import math
# from steganography import *
from MainHandler import MainHandler
from QRCodeHandler import QRCodeHandler
# import pyzbar.pyzbar as pyzbar

def make_app():
	return tornado.web.Application([
		(r"/api/linear", MainHandler),
		(r"/api/qrcode", QRCodeHandler)
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(14452)
	print ('listen 14452....')
	tornado.ioloop.IOLoop.current().start()