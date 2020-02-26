import tornado.ioloop
import tornado.web
import qrcode
import json
import pybase64
import math
import io
from PIL import Image
from pyzbar.pyzbar import decode
from PIL.PngImagePlugin import PngImageFile, PngInfo
import random

SETTING_BITS_NUM = 2500
CONFIG_QRCODE_WIDTH = 46

class DecodeHandler(tornado.web.RequestHandler):
	# extract a single bit from the rgb value
	def extract_qrcode_bit(self, rgbH, pageNum):
		rH, gH, bH = rgbH
		pixelBit = '1'
		if pageNum == 0:
			pixelBit = rH[7:8]
		elif pageNum == 1:
			pixelBit = rH[6:7]
		elif pageNum == 2:
			pixelBit = gH[7:8]
		elif pageNum == 3:
			pixelBit = gH[6:7]
		elif pageNum == 4:
			pixelBit = bH[7:8]
		elif pageNum == 5:
			pixelBit = bH[6:7]
			# the final value of this pixel
			# print(pixelBit, 'pixelBit == 0', pixelBit == '0', 'pixelBit == 1', pixelBit == '1')
		return pixelBit		

	# transform the int type to binary type
	def __int_to_bin(self, rgb):
		"""Convert an integer tuple to a binary (string) tuple.
		:param rgb: An integer tuple (e.g. (220, 110, 96))
		:return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
		"""
		# r, g, b, o = rgb
		return ('{0:08b}'.format(rgb[0]),
				'{0:08b}'.format(rgb[1]),
				'{0:08b}'.format(rgb[2]))	

	# judge whether the pixel is black
	def is_black(self, qrcodePixel):
		isBlack = True
		for i in range(len(qrcodePixel)):
			if qrcodePixel[i] == 255:
				isBlack = False
				break
		return isBlack

	# judge whether the pixel is white
	def is_white(self, qrcodePixel):
		isWhite = True
		for i in range(len(qrcodePixel)):
			if qrcodePixel[i] == 0:
				isWhite = False
				break
		return isWhite

	# extract the bit list from host image
	def extract_qrcode_bit_list(self, hostImage, hostImageHideChannel):
		hostImageWidth = hostImage.size[0]
		hostImageHeight = hostImage.size[1]
		hostImageMap = hostImage.load()
		qrCodeBitList = []
		for i in range(hostImageHideChannel):
			for j in range(hostImageWidth):
				for k in range(hostImageHeight):
					rgbH = self.__int_to_bin(hostImageMap[j, k])
					qrcodeBit = int(self.extract_qrcode_bit(rgbH, i))
					qrCodeBitList.append(qrcodeBit)
		return qrCodeBitList

	# parse the string information from the Qrcode image list
	def parse_encoding_str(self, extractQrcodeImgList):
		parseEncodingStr = ''
		for i in range(len(extractQrcodeImgList)):
			qrcodeImg = extractQrcodeImgList[i]
			qrcodeImgResult = decode(qrcodeImg)
			# qrcodeImg.show()
			if (len(qrcodeImgResult) > 0):
				parseEncodingStr = parseEncodingStr + qrcodeImgResult[0].data.decode('utf-8')
		return parseEncodingStr

	# assemble the qrcode image from the extracted bit list
	def revert_qrcode_image_list(self, extractQrcodeImgBitList, qrCodeCellMaxLen, qrCodeCellNum, qrCodeNum):
		qrCodeSideLen = qrCodeCellMaxLen * qrCodeCellNum
		qrcodeImgList = []
		qrcodeBitIndex = 0
		wholeQRcodeNum = math.floor(len(extractQrcodeImgBitList) / (qrCodeSideLen * qrCodeSideLen))
		print('extractQrcodeImgBit length', len(extractQrcodeImgBitList), 'qrCodeSideLen', qrCodeSideLen)
		print('qrCodeNum', qrCodeNum, 'wholeQrcodeNum', wholeQRcodeNum)
		if qrCodeNum > wholeQRcodeNum:
			qrCodeNum = wholeQRcodeNum
		for i in range(qrCodeNum):
			initQRCodeImg = Image.new(mode = "RGB", size = (qrCodeSideLen, qrCodeSideLen))
			initQRCodeImgMap = initQRCodeImg.load()
			for j in range(qrCodeSideLen):
				for k in range(qrCodeSideLen):
					if extractQrcodeImgBitList[qrcodeBitIndex] == 1:
						initQRCodeImgMap[j, k] = (255, 255, 255)
					elif extractQrcodeImgBitList[qrcodeBitIndex] == 0:
						initQRCodeImgMap[j, k] = (0, 0, 0)
					qrcodeBitIndex += 1
			# initQRCodeImg.show()
			# qrcodeImgStr = decode(initQRCodeImg)
			# print('qrcodeImgStr', qrcodeImgStr)
			qrcodeImgList.append(initQRCodeImg)
		return qrcodeImgList

	# correct the pixel color in the image
	def correct_qrcode_image_list(self, extractQrcodeImgList, qrCodeCellMaxLen):
		for i in range(len(extractQrcodeImgList)):
			qrcodeImg = extractQrcodeImgList[i]
			qrcodeImgMap = qrcodeImg.load()
			qrcodeImgWidth = qrcodeImg.size[0]
			# print('qrcodeImgWidth', qrcodeImgWidth)
			for cellX in range(0, (qrcodeImgWidth), qrCodeCellMaxLen):
				for cellY in range(0, (qrcodeImgWidth), qrCodeCellMaxLen):
					sumBlackBitNum = 0
					sumWhiteBitNum = 0
					cellColor = (255, 255, 255)
					for localX in range(qrCodeCellMaxLen):
						for localY in range(qrCodeCellMaxLen):
							pixelX = cellX + localX
							pixelY = cellY + localY
							if self.is_black(qrcodeImgMap[pixelX, pixelY]):
								sumBlackBitNum += 1
							if self.is_white(qrcodeImgMap[pixelX, pixelY]):
								sumWhiteBitNum += 1
					# correct bits in Qrcode
					# if sumWhiteBitNum != 0 and sumBlackBitNum != 0:
					# 		print('sumWhiteBitNum', sumWhiteBitNum, 'sumBlackBitNum', sumBlackBitNum)
					if sumBlackBitNum > sumWhiteBitNum:
						# set black
						cellColor = (0, 0, 0)
					elif sumBlackBitNum < sumWhiteBitNum:
						# set white
						cellColor = (255, 255, 255)
					else:
						# set the color (white or black) of this pixel randomly 
						if random.random() > 0.5:
							cellColor = (0, 0, 0)
						else:
							cellColor = (255, 255, 255)
					# set the pixel color of whole cell
					for localX in range(qrCodeCellMaxLen):
						for localY in range(qrCodeCellMaxLen):
							pixelX = cellX + localX
							pixelY = cellY + localY
							qrcodeImgMap[pixelX, pixelY] = cellColor
		return extractQrcodeImgList

	def assembleResultObj(self, messageType, message, extractStr=""):
		return {
			'type': messageType,
			'message': message,
			'extractStr': extractStr
		}

	def get(self):
		self.write("Hello, world")

	def post(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		requestBinary = self.request.body
		requestStr = requestBinary.decode()
		# transfrom the string parameters to the json object
		request_obj = json.loads(requestStr)
		# extract the host image str from the parameter object
		base64ImageStr = request_obj['image_uri']
		# image processing, divide the image data to two parts
		imgdatahead, imgdatacontent = base64ImageStr.split(",")
		# extract the parameters from the imgdatahead
		qrCodeNum = 0
		qrCodeCellNum = 179
		qrCodeCellMaxLen = 2
		# store the qrcode data into the imagedatacontent
		imgdata = pybase64.b64decode(imgdatacontent)
		hostImage = Image.open(io.BytesIO(imgdata))
		# evaluate whether the image is suitable for decoding
		# if hasattr(hostImage, 'text'):
		# 	EmbedInfoObj = hostImage.text
		# 	print('EmbedInfoObj', EmbedInfoObj)
		# 	if 'qrCodeNum' in EmbedInfoObj and 'qrCodeCellNum' in EmbedInfoObj and 'qrCodeCellMaxLen' in EmbedInfoObj:
		# 		qrCodeNum = int(EmbedInfoObj['qrCodeNum'])
		# 		qrCodeCellNum = int(EmbedInfoObj['qrCodeCellNum'])
		# 		qrCodeCellMaxLen = int(EmbedInfoObj['qrCodeCellMaxLen'])
		# 		print('qrCodeNum', qrCodeNum, 'qrCodeCellNum', qrCodeCellNum, 'qrCodeCellMaxLen', qrCodeCellMaxLen)
		# 	else:
		# 		notCompleteInfoMessage = 'The properties of this image are not complete.'
		# 		resultObj = self.assembleResultObj('error', notCompleteInfoMessage)
		# 		self.write(json.dumps(resultObj))
		# 		return
		# else:
		# 	notEmbedInfoMessage = 'The image does not embed other information.'
		# 	resultObj = self.assembleResultObj('error', notEmbedInfoMessage)
		# 	print('resultObj', resultObj)
		# 	resultObjStr = json.dumps(resultObj)
		# 	self.write(resultObjStr)
		# 	return
		hostImageWidth = hostImage.size[0]
		hostImageHeight = hostImage.size[1]
		hostImageHideChannel = 6
		# the parsing part, extract the bit list of qrcode image from the host image
		extractQrcodeImgBitList = self.extract_qrcode_bit_list(hostImage, hostImageHideChannel)
		print('finish extract_qrcode_bit_list')
		configQrcodeBitSize = CONFIG_QRCODE_WIDTH * CONFIG_QRCODE_WIDTH
		extractConfigQrcodeImgBitList = extractQrcodeImgBitList[:configQrcodeBitSize]
		qrcodeBorderWidth = 1
		configQrCodeModule = 1
		configQrCodeCellMaxLen = 2
		 # the side length of the qrcode content plus the border width
		configQrCodeCellNum = (configQrCodeModule * 4 + 17) + qrcodeBorderWidth * 2
		configExtractQrcodeImgList = self.revert_qrcode_image_list(extractConfigQrcodeImgBitList, configQrCodeCellMaxLen, configQrCodeCellNum, 1)
		extractConfigStr = self.parse_encoding_str(configExtractQrcodeImgList)
		[qrCodeNumStr, qrcodeModuleStr, qrCodeCellMaxLenStr] = extractConfigStr.split(' ')
		qrCodeNum = int(qrCodeNumStr)
		qrcodeModule = int(qrcodeModuleStr)
		qrCodeCellMaxLen = int(qrCodeCellMaxLenStr)
		qrCodeCellNum = (qrcodeModule * 4 + 17) + qrcodeBorderWidth * 2
		print('qrCodeNum', qrCodeNum, 'qrCodeCellNum', qrCodeCellNum, 'qrCodeCellMaxLen', qrCodeCellMaxLen)
		#
		print('length', len(extractQrcodeImgBitList))
		extractContentQrcodeImgBitList = extractQrcodeImgBitList[SETTING_BITS_NUM:]
		# revert the qrcode image list from the qrcode image bit list
		extractQrcodeImgList = self.revert_qrcode_image_list(extractContentQrcodeImgBitList, qrCodeCellMaxLen, qrCodeCellNum, qrCodeNum)
		print('finish extract_qrcode_bit_list')
		correctedExtractQrcodeImgList = self.correct_qrcode_image_list(extractQrcodeImgList, qrCodeCellMaxLen)
		print('finish qrcode correction')
		# extract the qrcode image to the inner string
		extractStr = self.parse_encoding_str(extractQrcodeImgList)
		print('finish parse_encoding_str')
		successMessage = "Extract the information from the image successfully!"
		# print('extractStr', extractStr)
		resultObj = self.assembleResultObj('success', successMessage, extractStr)
		self.write(json.dumps(resultObj))
		print('finish decoding')
		return
