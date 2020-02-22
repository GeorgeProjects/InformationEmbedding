import tornado.ioloop
import tornado.web

class QRCodeHandler(tornado.web.RequestHandler):
	def post(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		request_binary = self.request.body
		request_str = request_binary.decode()
		print(request_str)
		# qr = qrcode.QRCode (
		# 	# version = 15,
		# 	error_correction = qrcode.constants.ERROR_CORRECT_H,
		# 	box_size = 3,
		# 	border = 1
		# )
		# print(request_str)
		# qr.add_data(request_str)
		# qr.make(fit=True)
		# qrcodeImg = qr.make_image(fill_color="black", back_color="white")
		# qrcodeImg.show()
