import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
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
		# store the parameters into the imgdatahead
		
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
		qrCodeErrorCorrectionLevel = 'HIGH'
		# divide the specification data into several segments, and the length of each segment is fixed
		specDataList = list(chunkstring(specDataStr, qrCodeMaxCharacters))		
		# get the qrcode image list object
		qrcodeImgList = get_qrcode_image_list(specDataList, qrCodeCellMaxLen, qrCodeErrorCorrectionLevel)
		# transfrom the qrcode image to the bit list of qrcode 
		qrcodeImgBitList = compute_qrcode_bit_list(qrcodeImgList)
		# merge the bit list of qrcode into the host image and get the results
		embeddedHostImage = merge_qrcode_with_host_image2(qrcodeImgBitList, hostImage, hostImageHideChannel)
		# send the embedded host image back to the client
		buffered = io.BytesIO()
		embeddedHostImage.save(buffered, format="PNG")
		embeddedHostImageStr = pybase64.b64encode(buffered.getvalue())
		self.write(embeddedHostImageStr)

		# ###########################
		# # the parsing part, extract the bit list of qrcode image from the host image
		# extractQrcodeImgBitList = extract_qrcode_bit_list(hostImage, hostImageHideChannel)
		# # revert the qrcode image list from the qrcode image bit list
		# extractQrcodeImgList = revert_qrcode_image_list(extractQrcodeImgBitList, qrCodeCellMaxLen, qrCodeCellNum)
		# # extract the qrcode image to the inner string
		# extractEncodingStr = parse_encoding_str(extractQrcodeImgList)
		# print('extractEncodingStr', extractEncodingStr)
		# print('match', match)
		# print('qrcodeImgList Length', len(qrcodeImgList))

		# hostImage = merge_qrcode_with_host_image(qrcodeImgList, hostImage)
		# qrCodeImageArray = Steganography.parse_hidden_qrcode(hostImage, qrCodeCellNum, qrCodeCellMaxLen)
		# for i in range(qrCodeNum):
		# 	qrcodeImg = qrCodeImageArray[i]
		# 	qrcodeImg.show()
		# 	qrcodeImgStr = decode(qrcodeImg)
		# 	print(qrcodeImgStr)
		# buffered = io.BytesIO()
		# host_image.save(buffered, format="PNG")
		# host_image_str = pybase64.b64encode(buffered.getvalue())
		# self.write(host_image_str)
		# host_image.show()
		# print(len(spec_data_list))
		# print(spec_data_list[0])
		# qr = qrcode.QRCode(
		#     version = 40,
		#     error_correction = qrcode.constants.ERROR_CORRECT_L,
		#     box_size = 1,
		#     border = 1
		# )
		# qr.add_data(spec_data_list[0])
		# qr.make(fit=True)
		# qrcodeImg = qr.make_image(fill_color="black", back_color="white")
		# qrcodeImg.show()
		# print(qrcodeImg.size)
		# decodedData = zbarlight.scan_codes(['qrcode'], qrcodeImg)
		# # decodedData = pyzbar.decode(qrcodeImg)
		# print(decodedData)
		# 

	def get_qrcode_image_list(specDataList, qrCodeCellMaxLen, qrCodeErrorCorrectionLevel):
		qrcodeImgList = []
		for i in range(len(specDataList)):#
			# the range of the host image, compute the QR code image
			specData = specDataList[i]
			qr = qrcode.QRCode (
			    version = 40,
			    error_correction = qrcode.constants.ERROR_CORRECT_L, # the corresponding error correction level is Q
			    box_size = qrCodeCellMaxLen,
			    border = 1
			)
			qr.add_data(specData)
			qr.make(fit=True)
			qrcodeImg = qr.make_image(fill_color="black", back_color="white")
			# change the format of image object
			b = io.BytesIO()
			qrcodeImg.save(b,format="png")
			qrcodeImgPIL = Image.open(b)
			print('qrcodeImg', type(qrcodeImg), 'img3', type(qrcodeImgPIL))
			qrcodeImgStr = decode(qrcodeImgPIL)
			print('qrcodeImgStr', qrcodeImgStr)
			#
			# show out the qr code image
			# imgplot = plt.imshow(qrcodeImg)
			# plt.show()
			print('i', i)
			qrcodeImgList.append(qrcodeImg)
			# startPos = [qr_image_row_start_pixel, qr_image_column_start_pixel]
			# host_image = Steganography.merge(host_image, qrcodeImg, startPos, max_qr_image_length)
			# decodedData = zbarlight.scan_codes(['qrcode'], qrcodeImg)
		return qrcodeImgList
		
	
	# def parse_encoding_str(extractQrcodeImgList):
	# 	parseEncodingStr = ''
	# 	for i in range(len(extractQrcodeImgList)):
	# 		qrcodeImg = extractQrcodeImgList[i]
	# 		qrcodeImgResult = decode(qrcodeImg)
	# 		if (len(qrcodeImgResult) > 0):
	# 			parseEncodingStr = parseEncodingStr + qrcodeImgResult[0].data.decode('utf-8')
	# 	return parseEncodingStr

	# def revert_qrcode_image_list(extractQrcodeImgBitList, qrCodeCellMaxLen, qrCodeCellNum):
	# 	qrCodeSideLen = qrCodeCellMaxLen * qrCodeCellNum
	# 	qrcodeImgList = []
	# 	qrcodeBitIndex = 0
	# 	qrcodeNum = math.floor(len(extractQrcodeImgBitList) / (qrCodeSideLen * qrCodeSideLen))
	# 	for i in range(qrcodeNum):
	# 		initQRCodeImg = Image.new(mode = "RGB", size = (qrCodeSideLen, qrCodeSideLen))
	# 		initQRCodeImgMap = initQRCodeImg.load()
	# 		for j in range(qrCodeSideLen):
	# 			for k in range(qrCodeSideLen):
	# 				if extractQrcodeImgBitList[qrcodeBitIndex] == 1:
	# 					initQRCodeImgMap[j, k] = (255, 255, 255)
	# 				elif extractQrcodeImgBitList[qrcodeBitIndex] == 0:
	# 					initQRCodeImgMap[j, k] = (0, 0, 0)
	# 				qrcodeBitIndex += 1
	# 		# initQRCodeImg.show()
	# 		# qrcodeImgStr = decode(initQRCodeImg)
	# 		# print('qrcodeImgStr', qrcodeImgStr)
	# 		qrcodeImgList.append(initQRCodeImg)
	# 	return qrcodeImgList			

	# def chunkstring(string, length):
	#     return (string[0+i:length+i] for i in range(0, len(string), length))

	# def get_page_character_length(spec_data_str_len):
	# 	color_num = 3
	# 	# get the last second channel of the each channel of rgb color
	# 	bit_num = color_num * 2
	# 	spec_data_str_bit_len = math.ceil(spec_data_str_len / bit_num)
	# 	return spec_data_str_bit_len

	# def extract_qrcode_bit_list(hostImage, hostImageHideChannel):
	# 	hostImageWidth = hostImage.size[0]
	# 	hostImageHeight = hostImage.size[1]
	# 	hostImageMap = hostImage.load()
	# 	qrCodeBitList = []
	# 	for i in range(hostImageHideChannel):
	# 		for j in range(hostImageWidth):
	# 			for k in range(hostImageHeight):
	# 				rgbH = __int_to_bin(hostImageMap[j, k])
	# 				qrcodeBit = int(extract_qrcode_bit(rgbH, i))
	# 				qrCodeBitList.append(qrcodeBit)
	# 	return qrCodeBitList

	# def compute_qrcode_bit_list(qrcodeImgList):
	# 	qrcodeBitList = []
	# 	for i in range(len(qrcodeImgList)):
	# 		qrcodeImg = qrcodeImgList[i]
	# 		qrcodeSize = qrcodeImg.size
	# 		qrcodeImgMap = qrcodeImg.load()
	# 		for i in range(qrcodeSize[0]):
	# 			for j in range(qrcodeSize[1]):
	# 				if (qrcodeImgMap[i, j] == 0):
	# 					qrcodeBitList.append(0)
	# 				elif (qrcodeImgMap[i, j] == 255):
	# 					qrcodeBitList.append(1)
	# 	return qrcodeBitList

	# def merge_qrcode_with_host_image2 (qrcodeImgBitList, hostImage, hostImageHideChannel):
	# 	hostImageWidth = hostImage.size[0]
	# 	hostImageHeight = hostImage.size[1]
	# 	bitCount = 0
	# 	hostImageMap = hostImage.load()
	# 	for i in range(hostImageHideChannel):
	# 		for j in range(hostImageWidth):
	# 			for k in range(hostImageHeight):
	# 				if bitCount >= len(qrcodeImgBitList):
	# 					return hostImage
	# 				qrcodeImgBit = qrcodeImgBitList[bitCount]
	# 				# print(hostImageMap[j, k], qrcodeImgBitList[bitCount], i)
	# 				rgbH = __int_to_bin(hostImageMap[j, k])
	# 				# hostImageMap[j, k] = __merge_rgb_new(rgbH, qrcodeImgBit, i)
	# 				rgbH_new = __merge_rgb_new(rgbH, qrcodeImgBit, i)
	# 				hostImageMap[j, k] = __bin_to_int(rgbH_new)
	# 				bitCount = bitCount + 1

	# def __bin_to_int(rgb):
	# 	"""Convert a binary (string) tuple to an integer tuple.
	# 	:param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
	# 	:return: Return an int tuple (e.g. (220, 110, 96))
	# 	"""
	# 	r, g, b = rgb
	# 	return (int(r, 2),
	# 			int(g, 2),
	# 			int(b, 2))

	# def __int_to_bin(rgb):
	# 	"""Convert an integer tuple to a binary (string) tuple.
	# 	:param rgb: An integer tuple (e.g. (220, 110, 96))
	# 	:return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
	# 	"""
	# 	# r, g, b, o = rgb
	# 	return ('{0:08b}'.format(rgb[0]),
	# 			'{0:08b}'.format(rgb[1]),
	# 			'{0:08b}'.format(rgb[2]))

	# def __merge_rgb_new(rgbH, qrcodeImgBit, pageNum):
	# 	"""Merge two RGB tuples.
	# 	:param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
	# 	:param rgb2: Another string tuple
	# 	(e.g. ("00101010", "11101011", "00010110"))
	# 	:return: An integer tuple with the two RGB values merged.
	# 	"""
	# 	rH, gH, bH = rgbH	
	# 	rgb = rgbH
	# 	if pageNum == 0:
	# 		rgb = (rH[:7] + str(qrcodeImgBit), 
	# 				gH[:8],
	# 				bH[:8])
	# 	elif pageNum == 1:
	# 		rgb = (rH[:6] + str(qrcodeImgBit) + rH[7:8],
	# 				gH[:8],
	# 				bH[:8])
	# 	elif pageNum == 2:
	# 		rgb = (rH[:8],
	# 				gH[:7] + str(qrcodeImgBit),
	# 				bH[:8])
	# 	elif pageNum == 3:
	# 		rgb = (rH[:8],
	# 				gH[:6] + str(qrcodeImgBit) + gH[7:8],
	# 				bH[:8])
	# 	elif pageNum == 4:
	# 		rgb = (rH[:8],
	# 				gH[:8],
	# 				bH[:7] + str(qrcodeImgBit))
	# 	elif pageNum == 5:
	# 		rgb = (rH[:8],
	# 				gH[:8],
	# 				bH[:6] + str(qrcodeImgBit) + bH[7:8])
	# 	return rgb

	# def extract_qrcode_bit(rgbH, pageNum):
	# 	rH, gH, bH = rgbH
	# 	pixelBit = '1'
	# 	if pageNum == 0:
	# 		pixelBit = rH[7:8]
	# 	elif pageNum == 1:
	# 		pixelBit = rH[6:7]
	# 	elif pageNum == 2:
	# 		pixelBit = gH[7:8]
	# 	elif pageNum == 3:
	# 		pixelBit = gH[6:7]
	# 	elif pageNum == 4:
	# 		pixelBit = bH[7:8]
	# 	elif pageNum == 5:
	# 		pixelBit = bH[6:7]
	# 		# the final value of this pixel
	# 		# print(pixelBit, 'pixelBit == 0', pixelBit == '0', 'pixelBit == 1', pixelBit == '1')
	# 	return pixelBit

	# def merge_qrcode_with_host_image(qrcodeImgList, host_image):
	# 	hostImageWidth = host_image.size[0]
	# 	hostImageHeight = host_image.size[1]
	# 	hostImageBitNum = hostImageWidth * hostImageHeight
	# 	bitNum = 0
	# 	print(len(qrcodeImgList))
	# 	for i in range(len(qrcodeImgList)):
	# 		qrcodeImg = qrcodeImgList[i]
	# 		qrcodeImgWidth = qrcodeImg.size[0]
	# 		qrcodeImgHeight = qrcodeImg.size[1]
	# 		qrcodeImgBitNum = qrcodeImgWidth * qrcodeImgHeight
	# 		# qr code page num in the host image
	# 		qrcodePageNum = math.floor(bitNum / hostImageBitNum)
	# 		pageBitNum = bitNum % hostImageBitNum
	# 		# qr code position in the page, arrange the pixel along the row
	# 		qrcodePageRowNum = math.floor(pageBitNum / hostImageWidth)
	# 		qrcodePageColNum = pageBitNum % hostImageWidth
	# 		host_image = Steganography.merge_new(host_image, qrcodeImg, qrcodePageRowNum, qrcodePageColNum, qrcodePageNum)
	# 		bitNum = bitNum + qrcodeImgBitNum
	# 		print('bitNum', bitNum)
	# 	print('bitNum qrcode', bitNum)
	# 	print('bitNum host image', hostImageWidth * hostImageHeight * 6)
	# 	return host_image