#!/usr/local/bin/env python3

'''
Date: 10/31/20
Course: CS 231 - Advanced Python
Prof: Aaron Brick
Term: Fall 2020

Assignment #10 - Web service
Description:  Write an HTTP service that dynamically 
acquires a port number and serves a single copy of 
a memorable text to the first request that comes in. 
'''

import http.server
import socket

class Handler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response (200)
		self.send_header('Content-Type', 'text/plain')
		self.end_headers()
		quote = '''
		“Ready are you? What know you of ready? 
		For eight hundred years have I trained Jedi. 
		My own counsel will I keep on who is to be trained. 
		A Jedi must have the deepest commitment, the most serious mind. 
		This one a long time have I watched. 
		All his life has he looked away… to the future, to the horizon. 
		Never his mind on where he was. 
		Hmm? What he was doing. Hmph. Adventure. 
		Heh. Excitement. Heh. 
		A Jedi craves not these things. You are reckless.” 

		— Yoda

		'''
		self.wfile.write(quote.encode())

if __name__ == '__main__':
	# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s = socket.socket()
	s.bind(("0.0.0.0",0))
	s.listen(1)
	port = s.getsockname()[1]
	s.close()
	server = ( '', port )
	print(f"Server available on port: {port}")
	print(f"Press CTRL + \\ or CTRL + C to QUIT Server\n")
	print(f"Use this following to make a client request from another Hills terminal:\n")
	print(f"curl http://localhost:{port} -i")
	httpd = http.server.HTTPServer( server, Handler )
	httpd.serve_forever()
	httpd.server_close()