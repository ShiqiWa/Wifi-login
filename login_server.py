#-*- coding:utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
import sqlite3

class LoginHandler(BaseHTTPRequestHandler):
	# 接受POST请求，获取用户名和密码，然后查数据库，看是否有效
	def do_POST(self):
		# 获取用户名和密码
		content_type = cgi.parse_header(self.headers['content-type'])[0]
		if content_type == 'application/json':
			length = int(self.headers['content-length'])
			post_values = json.loads(self.rfile.read(length))
			print post_values['username'], post_values['password']
			username = "'" + post_values['username'] + "'"
			password = "'" + post_values['password'] + "'"
			conn = sqlite3.connect('test.db')
			c = conn.cursor()
			cursor = c.execute("SELECT password  from USER where username=" + "'" + post_values['username'] + "'")
			for row in cursor:
			   print row[0]
			   print row[0] == post_values['password']



if __name__ == '__main__':
    # Start a simple server, and loop forever
    server = HTTPServer(('localhost', 8888), LoginHandler)
    print("Starting server, use <Ctrl-C> to stop")
    server.serve_forever()