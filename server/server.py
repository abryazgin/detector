# -*- coding: utf-8 -*-
import SimpleHTTPServer
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time
import base64
import sys
from os import curdir
from os.path import join as pjoin

class Handler(BaseHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
		print "send header"
		if self.path == '/loadjpg':
			length = self.headers['content-length']
			data = self.rfile.read(int(length))

			store_path = pjoin(curdir, time.strftime("%Y-%m-%d_%H%M%S"), '.jpg')
			with open(store_path, 'w') as fh:
				fh.write(data)

			self.send_response(200)
		else:
			self.send_response(200)
			self.send_header('Content-type', 'text/html; charset=utf-8')
			self.end_headers()

    def do_AUTHHEAD(self):
        print "send header"
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=""')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
      
    def checkAuth(self):
		if self.headers.getheader('Authorization') == None:
			self.do_AUTHHEAD()
			self.wfile.write('no auth header received')
		else:
			# Для тестов логин пароль
			USER, PWD = "admin", "1"
			# YWRtaW46MQ==
			key = base64.b64encode(USER + ':' + PWD)
			if self.headers.getheader('Authorization') == 'Basic '+key:
				self.do_HEAD()
				print self.headers.getheader('Authorization')
			else:
				self.do_AUTHHEAD()
				self.wfile.write(u'Еще разок введите логин и пароль.!'.encode('utf-8'))
    
    def do_POST(self):
		print "POST!!!!!!!!!"
		self.checkAuth()
		
    def do_GET(self):
        self.checkAuth()
        
	
		

if __name__ == '__main__':
	HOST, PORT = "localhost", 10001
    
    # Создаем сервер на localhost:9999    
    # Do not automatically bind
	server = HTTPServer(("", 10001), Handler)	

	try:
		print time.asctime(), "Server Starts - %s:%s" % (HOST, PORT)
		# Запускаем сервер, который будет обрабатывать запросы, пока не прервем Ctrl-C
		server.serve_forever()
	except KeyboardInterrupt:
		pass 
	except Exception as e:
		print "Unexpected error:", e.message
	server.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST, PORT)
	
