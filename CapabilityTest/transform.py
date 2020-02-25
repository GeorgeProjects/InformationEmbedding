import json
f = open("qrcode_capability.txt", "r")
result = []
for line in open('qrcode_capability.txt'):
	line = f.readline()
	text = line.rstrip()
	if text != "":
		result.append(int(text))

qrcodeObj = {}
minV = 0
maxV = 40
vNum = 4
minModule = 21
for v in range(minV, maxV):
	minI = v * vNum
	maxI = minI + 4
	infoSize = result[minI:maxI]
	qrcodeInfoObj = {}
	capObj = {
		'L': infoSize[0],
		'M': infoSize[1],
		'Q': infoSize[2],
		'H': infoSize[3],
	}
	qrcodeInfoObj['capability'] = capObj
	qrcodeInfoObj['module'] = minModule
	qrcodeObj[str(v + 1)] = qrcodeInfoObj
	minModule += 4

with open('qrcodeObj.json', 'w', encoding='utf-8') as f:
    json.dump(qrcodeObj, f, ensure_ascii=False, indent=4)

    


