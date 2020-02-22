import tornado.ioloop
import tornado.web
import qrcode

class DecodeHandler(tornado.web.RequestHandler):
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
		qrCodeCellMaxLen = 3
		qrCodeCellNum = 179
		# store the qrcode data into the imagedatacontent
		imgdata = pybase64.b64decode(imgdatacontent)
		hostImage = Image.open(io.BytesIO(imgdata))
		hostImageWidth = hostImage.size[0]
		hostImageHeight = hostImage.size[1]
		hostImageHideChannel = 6
		# the parsing part, extract the bit list of qrcode image from the host image
		extractQrcodeImgBitList = extract_qrcode_bit_list(hostImage, hostImageHideChannel)
		# revert the qrcode image list from the qrcode image bit list
		extractQrcodeImgList = revert_qrcode_image_list(extractQrcodeImgBitList, qrCodeCellMaxLen, qrCodeCellNum)
		# extract the qrcode image to the inner string
		extractEncodingStr = parse_encoding_str(extractQrcodeImgList)
		return extractEncodingStr

	# extract the bit list from host image
	def extract_qrcode_bit_list(hostImage, hostImageHideChannel):
		hostImageWidth = hostImage.size[0]
		hostImageHeight = hostImage.size[1]
		hostImageMap = hostImage.load()
		qrCodeBitList = []
		for i in range(hostImageHideChannel):
			for j in range(hostImageWidth):
				for k in range(hostImageHeight):
					rgbH = __int_to_bin(hostImageMap[j, k])
					qrcodeBit = int(extract_qrcode_bit(rgbH, i))
					qrCodeBitList.append(qrcodeBit)
		return qrCodeBitList

	# parse the string information from the Qrcode image list
	def parse_encoding_str(extractQrcodeImgList):
		parseEncodingStr = ''
		for i in range(len(extractQrcodeImgList)):
			qrcodeImg = extractQrcodeImgList[i]
			qrcodeImgResult = decode(qrcodeImg)
			if (len(qrcodeImgResult) > 0):
				parseEncodingStr = parseEncodingStr + qrcodeImgResult[0].data.decode('utf-8')
		return parseEncodingStr

	# assemble the qrcode image from the extracted bit list
	def revert_qrcode_image_list(extractQrcodeImgBitList, qrCodeCellMaxLen, qrCodeCellNum):
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

	# transform the int type to binary type
	def __int_to_bin(rgb):
		"""Convert an integer tuple to a binary (string) tuple.
		:param rgb: An integer tuple (e.g. (220, 110, 96))
		:return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
		"""
		# r, g, b, o = rgb
		return ('{0:08b}'.format(rgb[0]),
				'{0:08b}'.format(rgb[1]),
				'{0:08b}'.format(rgb[2]))	

	# extract a single bit from the rgb value
	def extract_qrcode_bit(rgbH, pageNum):
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