import tornado.ioloop
import tornado.web
from EncodeHandler import EncodeHandler
from DecodeHandler import DecodeHandler

def make_app():
	return tornado.web.Application([
		(r"/api/encode", EncodeHandler),
		(r"/api/decode", DecodeHandler)
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(14452)
	print ('listen 14452....')
	tornado.ioloop.IOLoop.current().start()