import math
import json

f = open("qrcodeObj.json", "r")
qrcodeObjStr = f.read()
qrcodeObj = json.loads(qrcodeObjStr)

def computeMaxErrorBits(qrcodeModule, error, qrcodeCellNum):
	errorPercentageObj = {
		'1': 0.07,
		'2': 0.15, 
		'3': 0.25, 
		'4': 0.30
	}
	qrCodeCells = qrcodeCellNum * qrcodeCellNum
	if (qrCodeCells % 2 == 0):
		maxErrorBits = qrCodeCells // 2 - 1
	else:
		maxErrorBits = qrCodeCells // 2
	maxErrorBits = (qrcodeModule * 4 + 17) * (qrcodeModule * 4 + 17) * errorPercentageObj[str(error)] * maxErrorBits
	return maxErrorBits

def optimize(hostImageWidth, hostImageHeight, strLength, qrcodeObj, optimalCriteriaOrderArray=['maxErrorBits', 'qrcodeImageWidth', 'error', 'qrcodeCellNum', 'qrcodeModule']):
	resultArray = []
	hideChannel = 6
	for module in range(1, 41):
		for error in range(1, 5):
			qrcodeStrLength = qrcodeObj[str(module)]["capability"][str(error)]
			qrcodeNum = math.ceil(strLength / qrcodeStrLength)
			qrcodeCellNum = math.sqrt(hostImageWidth * hostImageHeight * hideChannel / qrcodeNum) // (module * 4 + 17)
			qrcodeImageWidth = (module * 4 + 17) * qrcodeCellNum
			maxErrorBits = computeMaxErrorBits(module, error, qrcodeCellNum)
			resultObj = {
				'qrcodeModule': module,
				'qrcodeCellNum': qrcodeCellNum,
				'error': error,
				'qrcodeImageWidth': qrcodeImageWidth,
				'maxErrorBits': maxErrorBits
			}
			resultArray.append(resultObj)
	# find the optimiza result
	optimalResultObj = {
		'qrcodeModule': 0,
		'qrcodeCellNum': 0,
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
def computeMinHostImageRatio(hostImageWidth, hostImageHeight, strLength):
	# the maximum module with lowest error correction
	qrcodeMaxStrLength = qrcodeObj['40']['capability']['1']
	qrcodeMaxWidth = 177 # the qrcode width of module 40
	hostImageHideChannel = 6
	qrcodeNum = math.ceil(strLength / qrcodeMaxStrLength)
	minHostImagePixel = math.ceil(qrcodeNum * qrcodeMaxWidth * qrcodeMaxWidth / hostImageHideChannel)
	hostImageSize = hostImageWidth * hostImageHeight
	if (hostImageSize < minHostImagePixel):
		ratio = math.sqrt(minHostImagePixel / hostImageSize)
		return ratio
	return 1

hostImageWidth = 1368
hostImageHeight = 776
strLength = 80286
minHostImageRatio = computeMinHostImageRatio(hostImageWidth, hostImageHeight, strLength)
print('minHostImageRatio', minHostImageRatio)
resizeHostImageWidth = math.ceil(hostImageWidth * minHostImageRatio)
resizeHostImageHeight = math.ceil(hostImageHeight * minHostImageRatio)
print('resizeHostImageHeight', resizeHostImageHeight, 'resizeHostImageWidth', resizeHostImageWidth)
optimalCriteriaOrderArray = ['maxErrorBits', 'qrcodeImageWidth', 'error', 'qrcodeCellNum', 'qrcodeModule'] # or 'maxErrorBits' or 'qrcodeImageWidth' or 'error' or 'qrcodeCellNum' or 'qrcodeModule'
optimalResultObj = optimize(resizeHostImageWidth, resizeHostImageHeight, strLength, qrcodeObj, optimalCriteriaOrderArray)
print('optimalResultObj', optimalResultObj)

