import tornado.ioloop
import tornado.web
import qrcode
import math
import io
import json
import pybase64
import math
from PIL import Image
from pyzbar.pyzbar import decode
from PIL.PngImagePlugin import PngImageFile, PngInfo

# define global variable
fileReader = open("qrcodeParamererObj.json", "r")
qrcodeParameterStr = fileReader.read()
qrcodeParameterObj = json.loads(qrcodeParameterStr)
errorCoorectionObj = {
	'1': 'ERROR_CORRECT_L',
	'2': 'ERROR_CORRECT_M', 
	'3': 'ERROR_CORRECT_Q', 
	'4': 'ERROR_CORRECT_H'
}

class EncodeHandler(tornado.web.RequestHandler):
	# segment the string
	def chunkstring(self, string, length):
	    return (string[0+i:length+i] for i in range(0, len(string), length))

	# compute the bit list according to the generated qrcode list	
	def compute_qrcode_bit_list(self, qrcodeImgList):
		qrcodeBitList = []
		for i in range(len(qrcodeImgList)):
			qrcodeImg = qrcodeImgList[i]
			qrcodeSize = qrcodeImg.size
			qrcodeImgMap = qrcodeImg.load()
			for i in range(qrcodeSize[0]):
				for j in range(qrcodeSize[1]):
					if (qrcodeImgMap[i, j] == 0):
						qrcodeBitList.append(0)
					elif (qrcodeImgMap[i, j] == 255):
						qrcodeBitList.append(1)
		return qrcodeBitList

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
	
	# transform the binary type to int type
	def __bin_to_int(self, rgb):
		"""Convert a binary (string) tuple to an integer tuple.
		:param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
		:return: Return an int tuple (e.g. (220, 110, 96))
		"""
		r, g, b = rgb
		return (int(r, 2),
				int(g, 2),
				int(b, 2))

	# merge the rgb value with the qrcodeImage bits
	def __merge_rgb_new(self, rgbH, qrcodeImgBit, pageNum):
		"""Merge two RGB tuples.
		:param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
		:param rgb2: Another string tuple
		(e.g. ("00101010", "11101011", "00010110"))
		:return: An integer tuple with the two RGB values merged.
		"""
		rH, gH, bH = rgbH	
		rgb = rgbH
		if pageNum == 0:
			rgb = (rH[:7] + str(qrcodeImgBit), 
					gH[:8],
					bH[:8])
		elif pageNum == 1:
			rgb = (rH[:6] + str(qrcodeImgBit) + rH[7:8],
					gH[:8],
					bH[:8])
		elif pageNum == 2:
			rgb = (rH[:8],
					gH[:7] + str(qrcodeImgBit),
					bH[:8])
		elif pageNum == 3:
			rgb = (rH[:8],
					gH[:6] + str(qrcodeImgBit) + gH[7:8],
					bH[:8])
		elif pageNum == 4:
			rgb = (rH[:8],
					gH[:8],
					bH[:7] + str(qrcodeImgBit))
		elif pageNum == 5:
			rgb = (rH[:8],
					gH[:8],
					bH[:6] + str(qrcodeImgBit) + bH[7:8])
		return rgb

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

	# merge the host image with the qrcode bit list
	def merge_qrcode_with_host_image (self, qrcodeImgBitList, hostImage, hostImageHideChannel):
		hostImageWidth = hostImage.size[0]
		hostImageHeight = hostImage.size[1]
		bitCount = 0
		hostImageMap = hostImage.load()
		for i in range(hostImageHideChannel):
			for j in range(hostImageWidth):
				for k in range(hostImageHeight):
					if bitCount >= len(qrcodeImgBitList):
						return hostImage
					qrcodeImgBit = qrcodeImgBitList[bitCount]
					rgbH = self.__int_to_bin(hostImageMap[j, k])
					rgbH_new = self.__merge_rgb_new(rgbH, qrcodeImgBit, i)
					hostImageMap[j, k] = self.__bin_to_int(rgbH_new)
					bitCount = bitCount + 1
		return hostImage

	# generate the qrcode list
	def get_qrcode_image_list(self, specDataList, qrCodeModule, qrCodeCellMaxLen, qrCodeErrorCorrectionLevel):
		qrcodeImgList = []
		for i in range(len(specDataList)):#
			# the range of the host image, compute the QR code image
			specData = specDataList[i]
			qr = qrcode.QRCode (
			    version = qrCodeModule,
			    error_correction = getattr(qrcode.constants, qrCodeErrorCorrectionLevel), # the corresponding error correction level is Q
			    box_size = qrCodeCellMaxLen,
			    border = 1
			)
			qr.add_data(specData)
			qr.make(fit=True)
			qrcodeImg = qr.make_image(fill_color="black", back_color="white")
			qrcodeImgList.append(qrcodeImg)
		return qrcodeImgList

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

	# assemble the qrcode image from the extracted bit list
	def revert_qrcode_image_list(self, extractQrcodeImgBitList, qrCodeCellMaxLen, qrCodeCellNum):
		qrCodeSideLen = qrCodeCellMaxLen * qrCodeCellNum
		qrcodeImgList = []
		qrcodeBitIndex = 0
		qrcodeNum = math.floor(len(extractQrcodeImgBitList) / (qrCodeSideLen * qrCodeSideLen))
		for i in range(qrcodeNum):
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
	
	# compute the maximum error correction bits
	def computeMaxErrorBits(self, qrcodeModule, error, qrcodeCellNum):
		errorPercentageObj = {
			'1': 0.07,
			'2': 0.15, 
			'3': 0.25, 
			'4': 0.30
		}
		qrCodeCells = qrcodeCellNum * qrcodeCellNum
		if (qrCodeCells % 2 == 0):
			maxErrorBits = math.floor(qrCodeCells / 2) - 1
		else:
			maxErrorBits = qrCodeCells / 2
		maxErrorBits = (qrcodeModule * 4 + 17) * (qrcodeModule * 4 + 17) * errorPercentageObj[str(error)] * maxErrorBits
		return maxErrorBits

	# compute the optimal host qrcode setting, including: 
	# 	'error correction level' and 
	# 	'module'
	def optimize(self, hostImageWidth, hostImageHeight, strLength, optimalCriteriaOrderArray=['maxErrorBits', 'qrcodeImageWidth', 'error', 'qrcodeCellNum', 'qrcodeModule']):
		resultArray = []
		hideChannel = 6
		for module in range(1, 41):
			for error in range(1, 5):
				qrcodeStrLength = qrcodeParameterObj[str(module)]["capability"][str(error)]
				qrcodeNum = math.ceil(strLength / qrcodeStrLength)
				qrCodeCellMaxLen = math.floor(math.sqrt(hostImageWidth * hostImageHeight * hideChannel / qrcodeNum) / (module * 4 + 17))
				qrcodeImageWidth = (module * 4 + 17) * qrCodeCellMaxLen
				maxErrorBits = self.computeMaxErrorBits(module, error, qrCodeCellMaxLen)
				resultObj = {
					'qrcodeModule': module,
					'qrCodeCellMaxLen': qrCodeCellMaxLen,
					'error': error,
					'qrcodeImageWidth': qrcodeImageWidth,
					'maxErrorBits': maxErrorBits
				}
				resultArray.append(resultObj)
		# find the optimiza result
		optimalResultObj = {
			'qrcodeModule': 0,
			'qrCodeCellMaxLen': 0,
			'error': 0,
			'qrcodeImageWidth': 0,
			'maxErrorBits': 0
		}
		for i in range(len(resultArray)):
			resultObj = resultArray[i]
			for kIndex in range(len(optimalCriteriaOrderArray)):
				if resultObj[optimalCriteriaOrderArray[kIndex]] > optimalResultObj[optimalCriteriaOrderArray[kIndex]]:
					optimalResultObj = resultObj
					break
				elif resultObj[optimalCriteriaOrderArray[kIndex]] < optimalResultObj[optimalCriteriaOrderArray[kIndex]]:
					break
		return optimalResultObj

	# resize an image
	# TODO the ratio of the host image
	def computeMinHostImageRatio(self, hostImageWidth, hostImageHeight, strLength):
		# the maximum module with lowest error correction
		qrcodeMaxStrLength = qrcodeParameterObj['40']['capability']['1']
		qrcodeMaxWidth = 177 # the qrcode width of module 40
		hostImageHideChannel = 6
		qrcodeNum = math.ceil(strLength / qrcodeMaxStrLength)
		minHostImagePixel = math.ceil(qrcodeNum * qrcodeMaxWidth * qrcodeMaxWidth / hostImageHideChannel)
		hostImageSize = hostImageWidth * hostImageHeight
		if (hostImageSize < minHostImagePixel):
			ratio = math.sqrt(minHostImagePixel / hostImageSize)
			return ratio
		return 1

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
		# extract the specification data from the parameter object
		specData = request_obj['spec_data']
		# image processing, divide the image data to two parts
		imgdatahead, imgdatacontent = base64ImageStr.split(",")
		# store the qrcode data into the imagedatacontent
		imgdata = pybase64.b64decode(imgdatacontent)
		hostImage = Image.open(io.BytesIO(imgdata))
		# targetImage = PngImageFile(io.BytesIO(imgdata))
		# print('targetImage', targetImage, 'hostImage', hostImage)
		hostImageWidth = hostImage.size[0]
		hostImageHeight = hostImage.size[1]
		# transform the json object to string specification
		specDataStr = json.dumps(specData)
		# the length of specifications
		specDataStrLen = len(specDataStr)
		# compute the minimum ratio of the host image
		minHostImageRatio = self.computeMinHostImageRatio(hostImageWidth, hostImageHeight, specDataStrLen)
		print('hostImageWidth', hostImageWidth, 'hostImageHeight', hostImageHeight, 'minHostImageRatio', minHostImageRatio)
		hostImageWidth = math.ceil(hostImageWidth * minHostImageRatio)
		hostImageHeight = math.ceil(hostImageHeight * minHostImageRatio)
		print('resizeHostImageWidth', hostImageWidth, 'resizeHostImageHeight', hostImageHeight)
		optimalCriteriaOrderArray = ['maxErrorBits', 'qrcodeImageWidth', 'error', 'qrCodeCellMaxLen', 'qrcodeModule'] # or 'maxErrorBits' or 'qrcodeImageWidth' or 'error' or 'qrCodeCellMaxLen' or 'qrcodeModule'
		optimalResultObj = self.optimize(hostImageWidth, hostImageHeight, specDataStrLen, optimalCriteriaOrderArray)
		print('optimalResultObj', optimalResultObj)
		print('specDataStrLen', specDataStrLen, 'hostImageWidth', hostImageWidth, 'hostImageHeight', hostImageHeight)
		# the visual channels of the qrcode to hide strings
		hostImageHideChannel = 6
		qrcodeModule = optimalResultObj['qrcodeModule']
		# compute the length of cells in QRCODE, #qrCodeCellNum#
		# 	 	  the length of pixels within a CELL, #qrCodeCellMaxLen#
		# 	 	  the error-correction LEVEL of QRCODE #qrCodeErrorCorrectionLevel, LOW/MIDDLE/QUARTILE/HIGH#
		# According to these three variables  
		#  derive the maximum characters within Qrcode 
		# TODO determine the string length of each qrcode
		qrcodeBorderWidth = 1
		 # the side length of the qrcode content plus the border width
		qrCodeCellNum = (qrcodeModule * 4 + 17) + qrcodeBorderWidth * 2
		# qrCodeCellMaxArea = math.floor(hostImageWidth * hostImageHeight * hostImageHideChannel / qrCodeNum)
		qrCodeCellMaxLen = optimalResultObj['qrCodeCellMaxLen']
		print('qrCodeCellMaxLen', qrCodeCellMaxLen)
		errorCorrectionIndex = optimalResultObj['error']
		print('errorCorrectionIndex', errorCorrectionIndex)
		qrCodeErrorCorrectionLevel = errorCoorectionObj[str(errorCorrectionIndex)]
		print('qrCodeErrorCorrectionLevel', qrCodeErrorCorrectionLevel)
		qrCodeModule = optimalResultObj['qrcodeModule']
		qrCodeMaxCharacters = qrcodeParameterObj[str(qrCodeModule)]['capability'][str(errorCorrectionIndex)]
		print('qrCodeMaxCharacters', qrCodeMaxCharacters)
		# the maximum number of qr code to store the information
		qrCodeNum = math.ceil(specDataStrLen / qrCodeMaxCharacters)
		# store the parameters into the imgdatahead
		# qrCodeCellNum
		# qrCodeCellMaxLen
		# divide the specification data into several segments, and the length of each segment is fixed
		specDataList = list(self.chunkstring(specDataStr, qrCodeMaxCharacters))	
		# get the qrcode image list object
		qrcodeImgList = self.get_qrcode_image_list(specDataList, qrCodeModule, qrCodeCellMaxLen, qrCodeErrorCorrectionLevel)
		print('finish get_qrcode_image_list')
		# transfrom the qrcode image to the bit list of qrcode 
		qrcodeImgBitList = self.compute_qrcode_bit_list(qrcodeImgList)
		print('finish compute_qrcode_bit_list')
		# merge the bit list of qrcode into the host image and get the results
		embeddedHostImage = self.merge_qrcode_with_host_image(qrcodeImgBitList, hostImage, hostImageHideChannel)
		print('finish merge_qrcode_with_host_image')
		# send the embedded host image back to the client
		# extractQrcodeImgBitList = self.extract_qrcode_bit_list(embeddedHostImage, hostImageHideChannel)
		# print('finish extract_qrcode_bit_list')		
		# revert the qrcode image list from the qrcode image bit list
		# extractQrcodeImgList = self.revert_qrcode_image_list(extractQrcodeImgBitList, qrCodeCellMaxLen, qrCodeCellNum)
		# print('finish revert_qrcode_image_list')		
		# extract the qrcode image to the inner string
		# extractEncodingStr = self.parse_encoding_str(extractQrcodeImgList)
		# print('finish parse_encoding_str', extractEncodingStr)
		# print(len(extractEncodingStr), len(specDataStr))
		qrCodeNum = len(qrcodeImgList)
		buffered = io.BytesIO()
		metadata = PngInfo()
		metadata.add_text("qrCodeNum", str(qrCodeNum))
		metadata.add_text("qrCodeCellNum", str(qrCodeCellNum))
		metadata.add_text("qrCodeCellMaxLen", str(qrCodeCellMaxLen))
		embeddedHostImage.save('host-image-test.png', pnginfo=metadata)
		embeddedHostImage = PngImageFile("host-image-test.png")
		embeddedHostImage.save(buffered, format="PNG", pnginfo=metadata)
		print('targetImage', embeddedHostImage, 'EmbedInfo', embeddedHostImage.text)
		embeddedHostImageStr = pybase64.b64encode(buffered.getvalue())
		self.write(embeddedHostImageStr)
