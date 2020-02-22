import tornado.ioloop
import tornado.web

class EncodeHandler(tornado.web.RequestHandler):
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
		hostImageWidth = hostImage.size[0]
		hostImageHeight = hostImage.size[1]
		# transform the json object to string specification
		specDataStr = json.dumps(specData)
		# the length of specifications
		specDataStrLen = len(specDataStr)
		# the visual channels of the qrcode to hide strings
		hostImageHideChannel = 6
		# compute the length of cells in QRCODE, #qrCodeCellNum#
		# 	 	  the length of pixels within a CELL, #qrCodeCellMaxLen#
		# 	 	  the error-correction LEVEL of QRCODE #qrCodeErrorCorrectionLevel, LOW/MIDDLE/QUARTILE/HIGH#
		# According to these three variables  
		#  derive the maximum characters within Qrcode 
		# TODO determine the string length of each qrcode
		qrcodeBorderWidth = 1
		 # the side length of the qrcode content plus the border width
		qrCodeCellNum = 177 + qrcodeBorderWidth * 2
		qrCodeMaxCharacters = 1273
		# the maximum number of qr code to store the information
		qrCodeNum = math.ceil(specDataStrLen / qrCodeMaxCharacters)
		qrCodeCellMaxArea = math.floor(hostImageWidth * hostImageHeight * hostImageHideChannel / qrCodeNum)
		qrCodeCellMaxLen = math.floor(math.sqrt(qrCodeCellMaxArea) / qrCodeCellNum)
		qrCodeErrorCorrectionLevel = 'ERROR_CORRECT_L'
		qrCodeVersion = 40
		# store the parameters into the imgdatahead
		# qrCodeCellNum
		# qrCodeCellMaxLen
		# divide the specification data into several segments, and the length of each segment is fixed
		specDataList = list(chunkstring(specDataStr, qrCodeMaxCharacters))		
		# get the qrcode image list object
		qrcodeImgList = get_qrcode_image_list(specDataList, qrCodeCellMaxLen, qrCodeErrorCorrectionLevel)
		# transfrom the qrcode image to the bit list of qrcode 
		qrcodeImgBitList = compute_qrcode_bit_list(qrcodeImgList)
		# merge the bit list of qrcode into the host image and get the results
		embeddedHostImage = merge_qrcode_with_host_image(qrcodeImgBitList, hostImage, hostImageHideChannel)
		# send the embedded host image back to the client
		buffered = io.BytesIO()
		embeddedHostImage.save(buffered, format="PNG")
		embeddedHostImageStr = pybase64.b64encode(buffered.getvalue())
		self.write(embeddedHostImageStr)

	# generate the qrcode list
	def get_qrcode_image_list(specDataList, qrCodeCellMaxLen, qrCodeErrorCorrectionLevel):
		qrcodeImgList = []
		for i in range(len(specDataList)):#
			# the range of the host image, compute the QR code image
			specData = specDataList[i]
			qr = qrcode.QRCode (
			    version = 40,
			    error_correction = getattr(qrcode.constants, qrCodeErrorCorrectionLevel), # the corresponding error correction level is Q
			    box_size = qrCodeCellMaxLen,
			    border = 1
			)
			qr.add_data(specData)
			qr.make(fit=True)
			qrcodeImg = qr.make_image(fill_color="black", back_color="white")
			qrcodeImgList.append(qrcodeImg)
		return qrcodeImgList
	
	# compute the bit list according to the generated qrcode list	
	def compute_qrcode_bit_list(qrcodeImgList):
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

	# merge the host image with the qrcode bit list
	def merge_qrcode_with_host_image (qrcodeImgBitList, hostImage, hostImageHideChannel):
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
					rgbH = __int_to_bin(hostImageMap[j, k])
					rgbH_new = __merge_rgb_new(rgbH, qrcodeImgBit, i)
					hostImageMap[j, k] = __bin_to_int(rgbH_new)
					bitCount = bitCount + 1
		return hostImage

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
	
	# transform the binary type to int type
	def __bin_to_int(rgb):
		"""Convert a binary (string) tuple to an integer tuple.
		:param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
		:return: Return an int tuple (e.g. (220, 110, 96))
		"""
		r, g, b = rgb
		return (int(r, 2),
				int(g, 2),
				int(b, 2))

	# merge the rgb value with the qrcodeImage bits
	def __merge_rgb_new(rgbH, qrcodeImgBit, pageNum):
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
	
	# segment the string
	def chunkstring(string, length):
	    return (string[0+i:length+i] for i in range(0, len(string), length))
